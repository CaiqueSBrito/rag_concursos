from app.graph.state import GraphState


def no_answer(state: GraphState):
    """
    Resposta final quando o fluxo esgota as tentativas de retrieval.
    """
    attempts = state.get("retrieval_attempt", 0)
    return {
        "documents": [],
        "retrieval_scores": [],
        "has_relevant_context": False,
        "generation": (
            "Nao encontrei contexto suficientemente relevante para responder "
            f"com seguranca apos {attempts} tentativas de busca."
        ),
    }
