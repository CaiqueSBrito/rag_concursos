from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.core.config import settings
from app.graph.state import GraphState
from app.repositories.chroma_repository import get_vectorstore


def retrieve(state: GraphState):
    """
    No que recupera documentos do banco vetorial.
    """
    print("[No: Retrieve] Buscando documentos relevantes...")

    question = state["question"]

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=settings.GEMINI_API_KEY,
    )
    vectorstore = get_vectorstore(embeddings=embeddings)

    results = vectorstore.similarity_search_with_relevance_scores(
        question,
        k=6,
        score_threshold=0.35,
    )
    documents = [doc for doc, _ in results]
    scores = [score for _, score in results]

    has_relevant_context = (
        len(documents) > 0
        and max(scores) >= 0.45
        and (sum(scores) / len(scores)) >= 0.40
    )

    return {
        "documents": documents,
        "retrieval_scores": scores,
        "question": question,
        "has_relevant_context": has_relevant_context,
    }
