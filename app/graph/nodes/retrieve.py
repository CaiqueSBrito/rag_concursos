from app.graph.state import GraphState
from app.repositories.chroma_repository import get_vectorstore
from app.services.embedding_service import get_embeddings_model


def retrieve(state: GraphState):
    """
    No que recupera documentos do banco vetorial.
    """
    print("[No: Retrieve] Buscando documentos relevantes...")

    question = state["question"]
    excluded_doc_ids = set(state.get("excluded_doc_ids", []))

    embeddings = get_embeddings_model()
    
    vectorstore = get_vectorstore(embeddings=embeddings)

    raw_results = vectorstore.similarity_search_with_relevance_scores(
        question,
        k=20,
        score_threshold=0.20,
    )

    filtered_results = []
    for doc, score in raw_results:
        chunk_id = doc.metadata.get("chunk_id")
        if chunk_id and chunk_id in excluded_doc_ids:
            continue
        filtered_results.append((doc, score))

    results = filtered_results[:6]
    documents = [doc for doc, _ in results]
    scores = [score for _, score in results]

    has_relevant_context = (
        len(documents) > 0
        and len(scores) > 0
        and max(scores) >= 0.45
        and (sum(scores) / len(scores)) >= 0.40
    )

    return {
        "documents": documents,
        "retrieval_scores": scores,
        "question": question,
        "has_relevant_context": has_relevant_context,
        "retrieval_attempt": state.get("retrieval_attempt", 0) + 1,
        "fallback_reason": "",
    }
