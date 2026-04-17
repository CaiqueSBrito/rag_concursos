from typing import TypedDict, List
from langchain_core.documents import Document

class GraphState(TypedDict):
    """
    Representa o estado do ciclo de vida de uma requisição RAG.
    """
    question: str       # Pergunta original
    documents: List[Document]  # Documentos recuperados do ChromaDB
    retrieval_scores: List[float] # Scores de similaridade dos documentos
    has_relevant_context: bool # Flag para indicar se o contexto é relevante
    generation: str     # Resposta final da LLM
