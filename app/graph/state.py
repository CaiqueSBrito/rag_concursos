from typing import List, TypedDict

from langchain_core.documents import Document


class GraphState(TypedDict):
    """
    Representa o estado do ciclo de vida de uma requisicao RAG.
    """

    question: str
    documents: List[Document]
    retrieval_scores: List[float]
    generation: str
    has_relevant_context: bool
    excluded_doc_ids: List[str]
    retrieval_attempt: int
    max_retrieval_attempts: int
    fallback_reason: str
