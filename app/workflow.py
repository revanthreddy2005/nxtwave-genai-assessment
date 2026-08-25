from langgraph.graph import END, START, StateGraph

from app.nodes import (
    evaluate_node,
    generate_node,
    regenerate_node,
)
from app.state import AgentState


def should_regenerate(state: AgentState) -> str:
    """
    Decide whether the workflow should regenerate the lesson
    or finish.
    """

    evaluation = state["evaluation"]
    retry_count = state.get("retry_count", 0)
    max_retries = state.get("max_retries", 2)

    # If the lesson passes all checks, finish.
    if evaluation.overall == "PASS":
        return "finish"

    # If the lesson fails but retries remain, regenerate.
    if retry_count < max_retries:
        return "regenerate"

    # Maximum retries reached.
    return "finish"


def build_workflow():
    """Build and compile the LangGraph workflow."""

    graph = StateGraph(AgentState)

    # Add nodes.
    graph.add_node("generate", generate_node)
    graph.add_node("evaluate", evaluate_node)
    graph.add_node("regenerate", regenerate_node)

    # Starting point.
    graph.add_edge(START, "generate")

    # Generate → Evaluate.
    graph.add_edge("generate", "evaluate")

    # Evaluate → either regenerate or finish.
    graph.add_conditional_edges(
        "evaluate",
        should_regenerate,
        {
            "regenerate": "regenerate",
            "finish": END,
        },
    )

    # Regenerate → Evaluate.
    graph.add_edge("regenerate", "evaluate")

    return graph.compile()