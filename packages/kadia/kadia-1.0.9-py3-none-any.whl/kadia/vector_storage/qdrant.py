import asyncio
import dataclasses
import hashlib
import logging
import time
from typing import (
    Iterable,
    List,
    Optional,
    Tuple,
)

import grpc
from aiokit import MultipleAsyncExecution
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchValue,
    PayloadSchemaType,
    PointStruct,
    Range,
    VectorParams,
)
from stc_geck.advices import BaseDocumentHolder

from ..document_chunker import Chunk, DocumentChunker, StoredChunk
from ..exceptions import QdrantStorageNotAvailableError
from .base import BaseVectorStorage


@dataclasses.dataclass
class ScoredChunk:
    chunk: StoredChunk
    score: float


@dataclasses.dataclass
class ScoredGroup:
    id: str
    scored_chunks: list[ScoredChunk]


class QdrantVectorStorage(BaseVectorStorage):
    def __init__(
        self,
        qdrant_config: dict,
        collection_name,
        force_recreate: bool = False,
    ):
        self.db = QdrantClient(**qdrant_config)
        self.collection_name = collection_name
        self.force_recreate = force_recreate
        self.is_existing = False

    def _exists_collection(self, collection_name):
        if self.is_existing:
            return True
        try:
            collections = self.db.get_collections()
        except grpc.RpcError:
            raise QdrantStorageNotAvailableError()
        for collection in collections.collections:
            if collection.name == collection_name:
                self.is_existing = True
                return True
        return False

    def _ensure_collection(self, collection_name, size):
        if not self.force_recreate:
            if self._exists_collection(collection_name):
                return
            self.db.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=size, distance=Distance.COSINE),
            )
        else:
            self.db.recreate_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=size, distance=Distance.COSINE),
            )
            self.force_recreate = False
        self.is_existing = True
        self.db.create_payload_index(
            collection_name=collection_name,
            field_name="document_id",
            field_schema=PayloadSchemaType.KEYWORD,
        )
        self.db.create_payload_index(
            collection_name=collection_name,
            field_name="issued_at",
            field_schema=PayloadSchemaType.INTEGER,
        )
        self.db.create_payload_index(
            collection_name=collection_name,
            field_name="type",
            field_schema=PayloadSchemaType.KEYWORD,
        )

    def get_by_field_values(
        self, field_values: Iterable[Tuple[str, str]], sort: bool = True
    ) -> List[Chunk]:
        if not self._exists_collection(self.collection_name):
            return []
        points, _ = self.db.scroll(
            collection_name=self.collection_name,
            scroll_filter=Filter(
                should=[
                    FieldCondition(key=field, match=MatchValue(value=value))
                    for (field, value) in field_values
                ],
            ),
            limit=2**31,
        )
        payloads = [Chunk(**point.payload) for point in points]
        if sort:
            return list(sorted(payloads, key=lambda x: (x.document_id, x.chunk_id)))
        return payloads

    def exists_by_field_value(self, field, value) -> bool:
        if not self._exists_collection(self.collection_name):
            return False
        points, _ = self.db.scroll(
            collection_name=self.collection_name,
            scroll_filter=Filter(
                should=[
                    FieldCondition(key=field, match=MatchValue(value=value)),
                ],
            ),
            with_payload=False,
            limit=1,
        )
        return len(points) > 0

    def _prepare_filter(self, field_values: Optional[Iterable[Tuple[str, str]]] = None,):
        if field_values:
            conditions = []
            for (field, value) in field_values:
                if isinstance(value, str):
                    conditions.append(
                        FieldCondition(key=field, match=MatchValue(value=value))
                    )
                else:
                    conditions.append(
                        FieldCondition(
                            key=field,
                            range=Range(
                                gte=value,
                                lte=value,
                            ),
                        )
                    )
            return Filter(should=conditions)

    def query(
        self,
        query_embedding,
        n_chunks: int,
        field_values: Optional[Iterable[Tuple[str, str]]] = None,
    ) -> List[ScoredChunk]:
        self._ensure_collection(
            collection_name=self.collection_name,
            size=len(query_embedding),
        )
        if n_chunks == 0:
            return []
        query_filter = self._prepare_filter(field_values=field_values)
        points = self.db.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            query_filter=query_filter,
            limit=n_chunks,
        )
        return [
            ScoredChunk(chunk=StoredChunk(**point.payload), score=point.score)
            for point in points
        ]

    def query_groups(
        self,
        query_embedding,
        n_chunks: int,
        group_by: str,
        group_size: int = 3,
        field_values: Optional[Iterable[Tuple[str, str]]] = None,
    ) -> list[ScoredGroup]:
        self._ensure_collection(
            collection_name=self.collection_name,
            size=len(query_embedding),
        )
        if n_chunks == 0:
            return []
        query_filter = self._prepare_filter(field_values=field_values)
        result = self.db.search_groups(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            query_filter=query_filter,
            group_by=group_by,
            group_size=group_size,
            limit=n_chunks,
        )
        return [
            ScoredGroup(
                id=group.id,
                scored_chunks=[
                    ScoredChunk(chunk=StoredChunk(**hit.payload), score=hit.score)
                    for hit in group.hits
                ],
            ) for group in result.groups
        ]

    def upsert(self, chunks: list[Chunk], embeddings: list[list[float]]):
        if not chunks:
            return
        embedding_size = len(embeddings[0])
        self._ensure_collection(
            collection_name=self.collection_name,
            size=embedding_size,
        )
        return self.db.upsert(
            collection_name=self.collection_name,
            points=[
                PointStruct(
                    id=hashlib.md5(
                        f"{chunk.document_id}@{chunk.chunk_id}".encode()
                    ).hexdigest(),
                    vector=embedding,
                    payload=dataclasses.asdict(
                        StoredChunk(
                            document_id=chunk.document_id,
                            field=chunk.field,
                            chunk_id=chunk.chunk_id,
                            title=chunk.title,
                            start_index=chunk.start_index,
                            length=chunk.length,
                            issued_at=chunk.issued_at,
                            updated_at=int(time.time()),
                        )
                    ),
                )
                for chunk, embedding in zip(chunks, embeddings)
            ],
        )

    async def _to_chunks(
        self,
        document_holder: BaseDocumentHolder,
        document_chunker: DocumentChunker,
        all_chunks: list[Chunk],
    ):
        all_chunks.extend(
            await asyncio.get_running_loop().run_in_executor(
                None, lambda d: document_chunker.to_chunks(d), document_holder
            )
        )

    async def get_missing_chunks(
        self,
        document_holders: List[BaseDocumentHolder],
        document_chunker: DocumentChunker,
        par: int = 16,
    ) -> List[Chunk]:
        all_chunks = []
        executor = MultipleAsyncExecution(par)
        for document_holder in document_holders:
            is_stored = await asyncio.get_running_loop().run_in_executor(
                None,
                lambda document_id: self.exists_by_field_value(
                    "document_id", document_id
                ),
                document_holder.get_id(),
            )
            if is_stored:
                logging.getLogger("statbox").info(
                    {
                        "action": "already_stored",
                        "mode": "kadia",
                        "document_id": document_holder.get_id(),
                    }
                )
                continue
            if (
                "abstract" not in document_holder.document
                and "content" not in document_holder.document
            ):
                logging.getLogger("statbox").info(
                    {
                        "action": "no_content",
                        "mode": "kadia",
                        "document_id": document_holder.get_id(),
                    }
                )
                continue
            try:
                await executor.execute(
                    self._to_chunks(document_holder, document_chunker, all_chunks)
                )
            except ValueError:
                logging.getLogger("statbox").info(
                    {
                        "action": "broken_content",
                        "mode": "kadia",
                        "document_id": document_holder.get_id(),
                    }
                )
        await executor.join()
        return all_chunks
