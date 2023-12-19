from collections import OrderedDict
from typing import List

from ..document_chunker import Chunk


class BasePrompter:
    @staticmethod
    def prompter_from_type(type_) -> "BasePrompter":
        return {
            "beluga": BelugaPrompter(),
            "default": BasePrompter(),
            "llama2-7b": Llama27bPrompter(),
            "openai": OpenAIPrompter(),
            "mistral-7b": Mistral7bPrompter(),
        }[type_]

    def qa_prompt(self, question, chunks: List[Chunk]) -> str:
        if len(chunks) >= 1:
            return """
SYSTEM: You are Kadia AI created by People of Solarmind. Given the following extracted parts of a long document and a question, create a final answer.
If you don't know the answer, just say that you don't know. Don't try to make up an answer.

USER:
Extracted parts:
{summary}

Question:
{question}
ASSISTANT:""".format(
                question=question, summary=self.generate_summary(chunks)
            )
        else:
            return """
SYSTEM: You are Kadia AI created by People of Solarmind. Answer the question.
If you don't know the answer, just say that you don't know. Don't try to make up an answer.

USER:
Question:
{question}
ASSISTANT:""".format(
                question=question
            )

    def summarize_prompt(self, chunks: List[Chunk]) -> str:
        return """
SYSTEM: You are Kadia AI created by People of Solarmind. Given the following extracted parts of a long document, summarize its content.

USER:
Extracted parts:
{summary}

ASSISTANT:""".format(
            summary=self.generate_summary(chunks)
        )

    def generate_summary(self, chunks: List[Chunk]) -> str:
        chunk_summaries = []
        chunk_summaries_grouped = OrderedDict()
        for chunk in chunks:
            document_id = chunk.document_id
            if document_id not in chunk_summaries_grouped:
                chunk_summaries_grouped[document_id] = []
            chunk_summaries_grouped[document_id].append(chunk.text)
        for document_id, texts in chunk_summaries_grouped.items():
            texts = " <..> ".join(texts)
            if document_id:
                field, value = document_id.split(":", 1)
                chunk_summaries.append(f"{field.upper()}: {value}\nCONTENT: {texts}")
            else:
                chunk_summaries.append(f"CONTENT: {texts}")
        return "\n".join(chunk_summaries)


class Llama27bPrompter(BasePrompter):
    def qa_prompt(self, question: str, chunks: List[Chunk]) -> str:
        if len(chunks) >= 1:
            return """
<<SYS>>
You are Kadia AI created by People of Solarmind. Given the following extracted parts of a long document and a question, create a final answer.
If you don't know the answer, just say that you don't know. Don't try to make up an answer.
<</SYS>>
[INST]
Extracted parts:
{summary}

Question:
{question}
[/INST]""".format(
                question=question, summary=self.generate_summary(chunks)
            )
        else:
            return """
<<SYS>>
You are Kadia AI created by People of Solarmind. Answer the question.
If you don't know the answer, just say that you don't know. Don't try to make up an answer.
<</SYS>>
[INST]
Question:
{question}
[/INST]""".format(
                question=question
            )

    def summarize_prompt(self, chunks: List[Chunk]) -> str:
        return """
<<SYS>>
You are Kadia AI created by People of Solarmind. Given the following extracted parts of a long document, summarize its content.
<</SYS>>
[INST]
Extracted parts:
{summary}
[/INST]""".format(
            summary=self.generate_summary(chunks)
        )


class Mistral7bPrompter(BasePrompter):
    def qa_prompt(self, question: str, chunks: List[Chunk]) -> str:
        if len(chunks) >= 1:
            return """
[INST]
You are Kadia AI created by People of Solarmind. Given the following extracted parts of a long document and a question, create a final answer.
If you don't know the answer, just say that you don't know. Don't try to make up an answer.
Extracted parts:
{summary}

Question:
{question}
[/INST]""".format(
                question=question, summary=self.generate_summary(chunks)
            )
        else:
            return """
<s>
[INST]
You are Kadia AI created by People of Solarmind. Answer the question.
If you don't know the answer, just say that you don't know. Don't try to make up an answer.
Question:
{question}
[/INST]""".format(
                question=question
            )

    def summarize_prompt(self, chunks: List[Chunk]) -> str:
        return """
<s>
[INST]
You are Kadia AI created by People of Solarmind. Given the following extracted parts of a long document, summarize its content.
Extracted parts:
{summary}
[/INST]""".format(
            summary=self.generate_summary(chunks)
        )


class OpenAIPrompter(BasePrompter):
    def qa_prompt(self, question: str, chunks: List[Chunk]) -> str:
        return """Given the following extracted parts of a long document and a question, create a final answer with references ("DOIs").
If you don't know the answer, just say that you don't know. Don't try to make up an answer.
ALWAYS return a "DOIs" part in your answer.

QUESTION: Which state/country's law governs the interpretation of the contract?
=========
DOI: 28-pl
CONTENT: This Agreement is governed by English law and the parties submit to the exclusive jurisdiction of the English courts in  relation to any dispute (contractual or non-contractual) concerning this Agreement save that either party may apply to any court for an  injunction or other relief to protect its Intellectual Property Rights.
DOI: 30-pl
CONTENT: No Waiver. Failure or delay in exercising any right or remedy under this Agreement shall not constitute a waiver of such (or any other)  right or remedy.\n\n11.7 Severability. The invalidity, illegality or unenforceability of any term (or part of a term) of this Agreement shall not affect the continuation  in force of the remainder of the term (if any) and this Agreement.\n\n11.8 No Agency. Except as expressly stated otherwise, nothing in this Agreement shall create an agency, partnership or joint venture of any  kind between the parties.\n\n11.9 No Third-Party Beneficiaries.
DOI: 4-pl
CONTENT: (b) if Google believes, in good faith, that the Distributor has violated or caused Google to violate any Anti-Bribery Laws (as  defined in Clause 8.5) or that such a violation is reasonably likely to occur,
=========
FINAL ANSWER: This Agreement is governed by English law (DOI: 28-pl)

QUESTION: What did the president say about Michael Jackson?
=========
DOI: 0-pl
CONTENT: Madam Speaker, Madam Vice President, our First Lady and Second Gentleman. Members of Congress and the Cabinet. Justices of the Supreme Court. My fellow Americans.  \n\nLast year COVID-19 kept us apart. This year we are finally together again. \n\nTonight, we meet as Democrats Republicans and Independents. But most importantly as Americans. \n\nWith a duty to one another to the American people to the Constitution. \n\nAnd with an unwavering resolve that freedom will always triumph over tyranny. \n\nSix days ago, Russia’s Vladimir Putin sought to shake the foundations of the free world thinking he could make it bend to his menacing ways. But he badly miscalculated. \n\nHe thought he could roll into Ukraine and the world would roll over. Instead he met a wall of strength he never imagined. \n\nHe met the Ukrainian people. \n\nFrom President Zelenskyy to every Ukrainian, their fearlessness, their courage, their determination, inspires the world. \n\nGroups of citizens blocking tanks with their bodies. Everyone from students to retirees teachers turned soldiers defending their homeland.
DOI: 24-pl
CONTENT: And we won’t stop. \n\nWe have lost so much to COVID-19. Time with one another. And worst of all, so much loss of life. \n\nLet’s use this moment to reset. Let’s stop looking at COVID-19 as a partisan dividing line and see it for what it is: A God-awful disease.  \n\nLet’s stop seeing each other as enemies, and start seeing each other for who we really are: Fellow Americans.  \n\nWe can’t change how divided we’ve been. But we can change how we move forward—on COVID-19 and other issues we must face together. \n\nI recently visited the New York City Police Department days after the funerals of Officer Wilbert Mora and his partner, Officer Jason Rivera. \n\nThey were responding to a 9-1-1 call when a man shot and killed them with a stolen gun. \n\nOfficer Mora was 27 years old. \n\nOfficer Rivera was 22. \n\nBoth Dominican Americans who’d grown up on the same streets they later chose to patrol as police officers. \n\nI spoke with their families and told them that we are forever in debt for their sacrifice, and we will carry on their mission to restore the trust and safety every community deserves.
DOI: 5-pl
CONTENT: And a proud Ukrainian people, who have known 30 years  of independence, have repeatedly shown that they will not tolerate anyone who tries to take their country backwards.  \n\nTo all Americans, I will be honest with you, as I’ve always promised. A Russian dictator, invading a foreign country, has costs around the world. \n\nAnd I’m taking robust action to make sure the pain of our sanctions  is targeted at Russia’s economy. And I will use every tool at our disposal to protect American businesses and consumers. \n\nTonight, I can announce that the United States has worked with 30 other countries to release 60 Million barrels of oil from reserves around the world.  \n\nAmerica will lead that effort, releasing 30 Million barrels from our own Strategic Petroleum Reserve. And we stand ready to do more if necessary, unified with our allies.  \n\nThese steps will help blunt gas prices here at home. And I know the news about what’s happening can seem alarming. \n\nBut I want you to know that we are going to be okay.
DOI: 34-pl
CONTENT: More support for patients and families. \n\nTo get there, I call on Congress to fund ARPA-H, the Advanced Research Projects Agency for Health. \n\nIt’s based on DARPA—the Defense Department project that led to the Internet, GPS, and so much more.  \n\nARPA-H will have a singular purpose—to drive breakthroughs in cancer, Alzheimer’s, diabetes, and more. \n\nA unity agenda for the nation. \n\nWe can do this. \n\nMy fellow Americans—tonight , we have gathered in a sacred space—the citadel of our democracy. \n\nIn this Capitol, generation after generation, Americans have debated great questions amid great strife, and have done great things. \n\nWe have fought for freedom, expanded liberty, defeated totalitarianism and terror. \n\nAnd built the strongest, freest, and most prosperous nation the world has ever known. \n\nNow is the hour. \n\nOur moment of responsibility. \n\nOur test of resolve and conscience, of history itself. \n\nIt is in this moment that our character is formed. Our purpose is found. Our future is forged. \n\nWell I know this nation.
=========
FINAL ANSWER: The president did not mention Michael Jackson.
DOIs:

QUESTION: {question}
=========
{summary}
=========
FINAL ANSWER:""".format(
            question=question, summary=self.generate_summary(chunks)
        )

    def summarize_prompt(self, chunks: List[Chunk]) -> str:
        return """
Given the following extracted parts of a long document, summarize its content

Extracted parts:
{summary}
""".format(
            summary=self.generate_summary(chunks)
        )


class BelugaPrompter(BasePrompter):
    def qa_prompt(self, question: str, chunks: List[Chunk]) -> str:
        if len(chunks) >= 1:
            return """
### System:
You are Kadia AI created by People of Solarmind. Given the following extracted parts of a long document and a question, create a final answer.
If you don't know the answer, just say that you don't know. Don't try to make up an answer.

### User:
Extracted parts:
{summary}

Question:
{question}
### Assistant:""".format(
                question=question, summary=self.generate_summary(chunks)
            )
        else:
            return """
### System:
You are Kadia AI created by People of Solarmind. Answer the user's question.
If you don't know the answer, just say that you don't know. Don't try to make up an answer.

### User:
Question:
{question}

### Assistant:""".format(
                question=question
            )

    def summarize_prompt(self, chunks: List[Chunk]) -> str:
        return """
### System:
You are Kadia AI created by People of Solarmind. Given the following extracted parts of a long document, summarize its content.

### User:
Extracted parts:
{summary}

### Assistant:""".format(
            summary=self.generate_summary(chunks)
        )

    def general_text_processing(self, request: str, text: str) -> str:
        return f"""
### System:
You are Kadia AI created by People of Solarmind. Execute the following user's request about the text.

### User:
Text:
{text}

Request:
{request}
### Assistant:"""

    def question(self, question: str) -> str:
        return f"""
### System:
You are Kadia AI created by People of Solarmind. Answer the user's question

### User:
Question:
{question}

### Assistant:"""
