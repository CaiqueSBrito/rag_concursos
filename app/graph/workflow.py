from langgraph.graph import StateGraph, START, END
from app.graph.state import GraphState
from app.graph.nodes.retrieve import retrieve
from app.graph.nodes.generate import generate
from app.graph.nodes.validate_context import validate_context

# Definimos o fluxo de trabalho (Workflow)
workflow = StateGraph(GraphState)

# Adicionamos os nós ao grafo
workflow.add_node("retrieve", retrieve)
workflow.add_node("generate", generate)
workflow.add_node("validate_context", validate_context)
workflow.add_node("fallback", fallback)

# Definimos as conexões (Arestas)
workflow.add_edge(START, "retrieve")
workflow.add_edge("retrieve", "validate_context")
workflow.add_conditional_edge("validate_context", lambda state: "generate" if state["has_relevant_context"] else "fallback")
workflow.add_edge("generate", END)

# Compilamos o grafo para ser executado
app_graph = workflow.compile()
