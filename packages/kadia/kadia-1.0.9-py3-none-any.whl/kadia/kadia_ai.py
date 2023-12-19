import asyncio
import io
import logging
import os.path
from dataclasses import dataclass
from typing import (
    Iterable,
    List,
    Literal,
    Optional,
    Tuple,
)

import confuse
import pypdf
import yaml
from aiokit import AioThing
from izihawa_utils.exceptions import BaseError
from izihawa_utils.file import mkdir_p
from stc_geck.advices import BaseDocumentHolder
from stc_geck.client import StcGeck

from .chains.map_reduce import (
    QAChain,
    SummarizeChain,
)
from .configs import ConfigGenerator
from .data_source.base import SourceDocument
from .data_source.geck_data_source import GeckDataSource
from .document_chunker import (
    Chunk,
    DocumentChunker,
)
from .model import KadiaModel
from aiokit import MultipleAsyncExecution
from .vector_storage.qdrant import (
    QdrantVectorStorage,
    ScoredChunk,
)


class DocumentNotFoundError(BaseError):
    pass


def print_color(text, color):
    print("\033[38;5;{}m{}\033[0m".format(color, text))


@dataclass
class KadiaResponse:
    answer: str
    chunks: List[Chunk]


class KadiaAI(AioThing):
    def __init__(
        self,
        home_path: Optional[str] = None,
        geck: Optional[StcGeck] = None,
    ):
        """
        Main Kadia class that manages AI operations

        :param home_path: path to config and/or embeddings directory
        :param geck: an instance of GECK
        """
        super().__init__()
        self.home_path = self.get_home_path(home_path)
        config = confuse.Configuration("kadia", __name__)
        config_path = self.ensure_config()
        config.set_file(config_path)

        self.model = KadiaModel(config["model"])
        self.document_chunker = DocumentChunker(
            text_splitter=self.model.text_splitter,
            add_metadata=self.model.config["text_splitter"]["add_metadata"].get(bool),
        )

        self.geck = geck
        if not self.geck:
            self.geck = StcGeck(
                ipfs_http_base_url=config["ipfs"]["http"]["base_url"].get(str),
                grpc_api_endpoint=config["summa"]["endpoint"].get(str),
                timeout=600,
            )
            self.starts.append(self.geck)

        self.data_source = GeckDataSource(self.geck)
        self.vector_storage = QdrantVectorStorage(
            qdrant_config=config["qdrant"],
            collection_name=self.model.get_embeddings_id(),
            embedding_function=self.model.embed_documents,
            force_recreate=config["qdrant"]["force_recreate"].get(bool),
        )

    async def _get_missing_chunks_job(self, all_chunks, document):
        document_chunks = await self.generate_chunks_from_document(document)
        all_chunks.extend(document_chunks)

    async def _get_missing_chunks(
        self,
        documents: List[SourceDocument],
        skip_downloading_pdf: bool = True,
        par: int = 16,
    ) -> List[Chunk]:
        all_chunks = []
        executor = MultipleAsyncExecution(par)
        for document in documents:
            is_stored = await asyncio.get_running_loop().run_in_executor(
                None,
                lambda document_id: self.vector_storage.exists_by_field_value(
                    "document_id", document_id
                ),
                document.document_id,
            )
            if is_stored:
                logging.getLogger("statbox").info(
                    {
                        "action": "already_stored",
                        "mode": "kadia",
                        "document_id": document.document_id,
                    }
                )
                continue
            if skip_downloading_pdf and "content" not in document.document:
                logging.getLogger("statbox").info(
                    {
                        "action": "no_content",
                        "mode": "kadia",
                        "document_id": document.document_id,
                    }
                )
                continue
            try:
                await executor.execute(
                    self._get_missing_chunks_job(all_chunks, document)
                )
            except ValueError:
                logging.getLogger("statbox").info(
                    {
                        "action": "broken_content",
                        "mode": "kadia",
                        "document_id": document.document_id,
                    }
                )
        await executor.join()
        return all_chunks

    async def _search_in_vector_storage(
        self,
        query: str,
        n_chunks: int = 3,
        field_values: Optional[Iterable[Tuple[str, str]]] = None,
        minimum_score: float = 0.5,
    ) -> List[ScoredChunk]:
        logging.getLogger("statbox").info(
            {
                "action": "query",
                "mode": "kadia",
                "query": query,
                "n_chunks": n_chunks,
                "field_values": field_values,
            }
        )
        chunks = await asyncio.get_running_loop().run_in_executor(
            None,
            lambda: self.vector_storage.query(
                self.model.embedder.embed_query(query),
                n_chunks=n_chunks,
                field_values=field_values,
            ),
        )
        filtered_chunks = []
        for chunk in chunks:
            if chunk.score > minimum_score:
                filtered_chunks.append(chunk)
        logging.getLogger("statbox").info(
            {
                "action": "query",
                "mode": "kadia",
                "found": len(filtered_chunks),
                "minimum_score": minimum_score,
            }
        )
        return filtered_chunks

    def get_home_path(self, home_path: str) -> str:
        """
        Expands path to config and/or embeddings directory and ensures the directory existence

        :param home_path:
        :return:
        """
        if home_path is None:
            home_path = os.environ.get("KADIA_HOME", "~/.kadia")
        home_path = os.path.expanduser(home_path)
        if not os.path.exists(home_path):
            mkdir_p(home_path)
        return home_path

    def ensure_config(
        self,
        ipfs_http_base_url: str = "http://127.0.0.1:8080",
        summa_endpoint: str = "127.0.0.1:10082",
        qdrant_base_url: str = "http://127.0.0.1",
        llm_name: Literal[
            "llama-2-7b",
            "llama-2-7b-uncensored",
            "llama-2-13b",
            "openai",
            "petals-llama-2-70b",
            "petals-stable-beluga",
            "mistral-7b",
        ] = "mistral-7b",
        embedder_name: Literal[
            "instructor-xl", "openai", "bge-small-en"
        ] = "bge-small-en",
        device: str = "cpu",
        gpu_layers: int = 50,
        force: bool = False,
    ):
        """
        Write config to $KADIA_HOME/config.yaml
        :param ipfs_http_base_url: IPFS HTTP base url, i.e. `http://127.0.0.1:8080`
        :param summa_endpoint: Summa endpoint, i.e. `127.0.0.1:10082`
        :param qdrant_base_url:
        :param llm_name: 'llama-2-7b', 'llama-2-7b-uncensored', 'llama-2-13b', 'openai', 'petals-llama-2-70b', 'petals-stable-beluga', 'mistral-7b'
        :param embedder_name: 'instructor-xl', 'openai', 'bge-small-en''
        :param device: 'cpu' or 'cuda'
        :param gpu_layers: number of layers to enabled offloading part of calculations to GPU
        :param force: overwrite even if config already exists
        :return:
        """
        config_path = os.path.join(self.home_path, "config.yaml")
        if not os.path.exists(config_path) or force:
            config = {
                "ipfs": {
                    "http": {
                        "base_url": ipfs_http_base_url,
                    }
                },
                "model": ConfigGenerator.default_config(
                    llm_name=llm_name,
                    embedder_name=embedder_name,
                    device=device,
                    gpu_layers=gpu_layers,
                ),
                "qdrant": {
                    "url": qdrant_base_url,
                    "prefer_grpc": True,
                },
                "summa": {
                    "endpoint": summa_endpoint,
                },
            }
            with open(config_path, "w") as f:
                f.write(yaml.dump(config, default_flow_style=False))
        return config_path

    async def resolve_document_content(self, document: SourceDocument) -> Optional[str]:
        """
        Retrieves document content from `content` field or from underlying PDF file.

        :param document:
        :return:
        """
        document = document.document
        if "content" in document:
            return document["content"]
        document_holder = BaseDocumentHolder(document)
        # ToDo: should also utilize epub links
        if pdf_link := document_holder.get_links().get_link_with_extension("pdf"):
            file_content = await self.geck.download(pdf_link["cid"])
            pdf_reader = pypdf.PdfReader(io.BytesIO(file_content))
            return "\n".join(page.extract_text() for page in pdf_reader.pages)
        return

    async def upsert_documents(
        self, documents: List[SourceDocument], skip_downloading_pdf: bool = True
    ):
        """
        Upsert documents into vector storage

        :param documents:
        :param skip_downloading_pdf:
        :return:
        """

        if not documents:
            return
        chunks = await self._get_missing_chunks(
            documents, skip_downloading_pdf=skip_downloading_pdf
        )
        if chunks:
            logging.getLogger("statbox").info(
                {
                    "action": "add_full_documents",
                    "mode": "kadia",
                    "n": len(chunks),
                }
            )
            await asyncio.get_running_loop().run_in_executor(
                None, lambda: self.vector_storage.upsert(chunks)
            )
            logging.getLogger("statbox").info(
                {
                    "action": "added_full_documents",
                    "mode": "kadia",
                    "n": len(chunks),
                }
            )

    async def upsert_document_by_query(
        self, query: str, skip_downloading_pdf: bool = True
    ):
        """
        Query documents from data source and upsert them into vector storage

        :param query:
        :param skip_downloading_pdf:
        :return:
        """
        documents = await self.data_source.search_documents(query, limit=1)
        if not documents:
            raise DocumentNotFoundError(id_=query)
        await self.upsert_documents(
            documents, skip_downloading_pdf=skip_downloading_pdf
        )
        return documents[0].document_id

    async def search_documents(
        self, query: str, n_documents: int = 10, use_only_keywords: bool = False
    ) -> List[SourceDocument]:
        if not n_documents:
            return []

        # Keywords extraction is required to reduce the number STC access requests (more words => more network requests)
        if use_only_keywords and self.model.keyword_extractor:
            logging.getLogger("statbox").info(
                {
                    "action": "extract_keywords",
                    "mode": "kadia",
                    "query": query,
                }
            )
            keywords = await asyncio.get_running_loop().run_in_executor(
                None,
                lambda: self.model.keyword_extractor.extract_keywords(
                    query,
                    keyphrase_ngram_range=(1, 1),
                ),
            )

            keywords = list(
                map(
                    lambda x: x[1][0],
                    filter(lambda x: x[1][1] > 0.5 or x[0] < 2, enumerate(keywords)),
                )
            )
            query = " ".join(keywords)

        logging.getLogger("statbox").info(
            {
                "action": "query",
                "mode": "kadia",
                "query": query,
            }
        )
        documents = await self.data_source.search_documents(
            query=query, limit=n_documents
        )
        return documents

    async def get_documents_from_chunks(self, chunks):
        """
        Return original documents using GECK and identifiers from chunks

        :param chunks:
        :return:
        """
        ids = set([chunk["document_id"] for chunk in chunks])
        subqueries = []
        for id_ in ids:
            field, value = id_.split(":", 1)
            subqueries.append(
                {"query": {"match": {"value": f'{field}:"{value}"'}}, "occur": "should"}
            )

        search_request = {
            "index_alias": "nexus_science",
            "query": {"boolean": {"subqueries": subqueries}},
            "collectors": [{"top_docs": {"limit": len(subqueries)}}],
            "is_fieldnorms_scoring_enabled": False,
        }
        return await self.geck.get_summa_client().search_documents(search_request)

    async def semantic_search_in_documents(
        self,
        query: str,
        documents: List[SourceDocument],
        n_chunks: int = 10,
        minimum_score: float = 0.5,
        skip_downloading_pdf: bool = True,
    ) -> List[ScoredChunk]:
        await self.upsert_documents(
            documents, skip_downloading_pdf=skip_downloading_pdf
        )
        return await self._search_in_vector_storage(
            query=query,
            n_chunks=n_chunks,
            field_values=[
                ("document_id", document.document_id) for document in documents
            ],
            minimum_score=minimum_score,
        )

    async def semantic_search(
        self,
        query: str,
        n_chunks: int = 10,
        n_documents: int = 30,
        minimum_score: float = 0.5,
        skip_downloading_pdf: bool = True,
        use_only_keywords: bool = True,
    ) -> List[ScoredChunk]:
        """
        Flow for retrieving chunks by chunking documents relevant to `query`

        :param skip_downloading_pdf:
        :param query:
        :param n_chunks:
        :param n_documents:
        :param minimum_score:
        :param use_only_keywords:
        :return:
        """
        documents = await self.search_documents(
            query, n_documents, use_only_keywords=use_only_keywords
        )
        await self.upsert_documents(
            documents, skip_downloading_pdf=skip_downloading_pdf
        )
        return await self._search_in_vector_storage(
            query=query,
            n_chunks=n_chunks,
            minimum_score=minimum_score,
        )

    async def chat_document(
        self, document_id: str, query: str, n_chunks: int, minimum_score: float = 0.5
    ) -> KadiaResponse:
        """
        Flow for getting document by `document_id` and finding answer in this document.

        :param document_id:
        :param query:
        :param n_chunks:
        :param minimum_score:
        :return:
        """

        # Hint: `document_id` is a valid query in STC
        document_id = await self.upsert_document_by_query(
            str(document_id), skip_downloading_pdf=False
        )
        scored_chunks = await self._search_in_vector_storage(
            query=query,
            n_chunks=n_chunks,
            field_values=(("document_id", document_id),),
            minimum_score=minimum_score,
        )
        chunks = [scored_chunk.chunk for scored_chunk in scored_chunks]

        chain = QAChain(query=query, llm_manager=self.model.llm_manager)
        answer = await asyncio.get_running_loop().run_in_executor(
            None,
            lambda: chain.process(chunks),
        )

        return KadiaResponse(answer=answer.strip(), chunks=chunks)

    async def chat_science(
        self, query: str, n_chunks: int, n_documents: int, minimum_score: float = 0.5
    ) -> KadiaResponse:
        """
        Flow for searching relevant document for the query and then answering query using documents and LLM

        :param query:
        :param n_chunks:
        :param n_documents:
        :param minimum_score:
        :return:
        """
        if n_chunks:
            scored_chunks = await self.semantic_search(
                query=query,
                n_chunks=n_chunks,
                n_documents=n_documents,
                minimum_score=minimum_score,
            )
            chunks = [scored_chunk.chunk for scored_chunk in scored_chunks]

            chain = QAChain(query=query, llm_manager=self.model.llm_manager)
            answer = await asyncio.get_running_loop().run_in_executor(
                None,
                lambda: chain.process(chunks),
            )
            return KadiaResponse(answer=answer.strip(), chunks=chunks)
        else:
            answer = await asyncio.get_running_loop().run_in_executor(
                None,
                lambda: self.model.llm_manager.process(
                    self.model.llm_manager.prompter.question(query)
                ),
            )
            return KadiaResponse(answer=answer.strip(), chunks=[])

    async def summarize_document(self, document_query):
        document_id = await self.upsert_document_by_query(
            document_query, skip_downloading_pdf=False
        )
        chunks = await asyncio.get_running_loop().run_in_executor(
            None,
            lambda: self.vector_storage.get_by_field_values(
                field_values=(("document_id", document_id),)
            ),
        )
        chain = SummarizeChain(llm_manager=self.model.llm_manager)
        answer = await asyncio.get_running_loop().run_in_executor(
            None,
            lambda: chain.process(chunks),
        )
        return KadiaResponse(answer=answer.strip(), chunks=chunks)

    async def general_text_processing(self, request, text):
        """
        Process user's request using text

        :param request:
        :param text:
        :return:
        """
        answer = await asyncio.get_running_loop().run_in_executor(
            None,
            lambda: self.model.llm_manager.process(
                self.model.llm_manager.prompter.general_text_processing(
                    request=request, text=text
                )
            ),
        )
        return KadiaResponse(answer=answer.strip(), chunks=[])
