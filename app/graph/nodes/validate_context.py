from app.graph.state import GraphState


def validate_context(state: GraphState):
    scores = state["retrieval_scores"]
    documents = state["documents"]

    if not documents:
        return {"has_relevant_context": False}
    
    max_score = max(scores)
    avg_score = sum(scores) / len(scores)

    has_relevant_context = max_score >= 0.45 and avg_score >= 0.40

    return {"has_relevant_context": has_relevant_context}