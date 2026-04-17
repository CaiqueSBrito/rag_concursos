from langgraph.graph import END, START, StateGraph

from app.graph.nodes.fallback import fallback
from app.graph.nodes.generate import generate
from app.graph.nodes.no_answer import no_answer
from app.graph.nodes.retrieve import retrieve
from app.graph.nodes.validate_context import validate_context
from app.graph.state import GraphState


workflow = StateGraph(GraphState)

workflow.add_node("retrieve", retrieve)
workflow.add_node("generate", generate)
workflow.add_node("validate_context", validate_context)
workflow.add_node("fallback", fallback)
workflow.add_node("no_answer", no_answer)

workflow.add_edge(START, "retrieve")
workflow.add_edge("retrieve", "validate_context")
workflow.add_conditional_edges("validate_context", lambda state: "generate" if state["has_relevant_context"] else "fallback",)
workflow.add_conditional_edges("fallback", lambda state: ("retrieve" if state["retrieval_attempt"] < state["max_retrieval_attempts"] else "no_answer"),)
workflow.add_edge("generate", END)
workflow.add_edge("no_answer", END)

app_graph = workflow.compile()
