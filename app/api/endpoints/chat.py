from fastapi import APIRouter
from app.graph.workflow import app_graph

router = APIRouter()

@router.post("/chat")
async def chat_rag(question: str):
    """
    Endpoint principal para conversar com o RAG.
    O LangGraph orquestra o fluxo de busca e geração.
    """
    print(f"🚀 [API] Nova pergunta recebida: {question}")
    
    # Preparamos o estado inicial do grafo
    initial_state = {"question": question, "documents": [], "generation": ""}
    
    # Invocamos o grafo (isso dispara automaticamente o retrieve e depois o generate)
    final_state = app_graph.invoke(initial_state)
    
    return {
        "resposta": final_state["generation"],
        "documentos_usados": [doc.metadata for doc in final_state["documents"]]
    }
