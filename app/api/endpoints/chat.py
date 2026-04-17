from fastapi import APIRouter

from app.graph.state import GraphState
from app.graph.workflow import app_graph

router = APIRouter()


@router.post("/chat")
async def chat_rag(question: str):
    """
    Endpoint principal para conversar com o RAG.
    O LangGraph orquestra o fluxo de busca e geracao.
    """
    print(f"[API] Nova pergunta recebida: {question}")

    initial_state = GraphState(
        question=question,
        documents=[],
        retrieval_scores=[],
        generation="",
        has_relevant_context=False,
        excluded_doc_ids=[],
        retrieval_attempt=0,
        max_retrieval_attempts=3,
        fallback_reason="",
    )

    final_state = app_graph.invoke(initial_state)

    return {
        "resposta": final_state["generation"],
        "documentos_usados": [doc.metadata for doc in final_state["documents"]],
        "tentativas_retrieval": final_state["retrieval_attempt"],
        "fallback_reason": final_state["fallback_reason"],
        "contexto_aprovado": final_state["has_relevant_context"],
    }
