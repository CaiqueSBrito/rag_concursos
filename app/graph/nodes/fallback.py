from app.graph.state import GraphState


def fallback(state: GraphState):
    """
    Descarta o contexto reprovado da tentativa atual e prepara novo retrieval.
    """
    rejected_ids = [
        doc.metadata.get("chunk_id")
        for doc in state.get("documents", [])
        if doc.metadata.get("chunk_id")
    ]
    previous_excluded = state.get("excluded_doc_ids", [])

    return {
        "documents": [],
        "retrieval_scores": [],
        "has_relevant_context": False,
        "excluded_doc_ids": list(set(previous_excluded + rejected_ids)),
        "fallback_reason": "contexto_reprovado",
    }
