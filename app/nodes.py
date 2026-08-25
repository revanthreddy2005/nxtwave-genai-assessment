from app.evaluator import evaluate_lesson
from app.generator import generate_lesson
from app.state import AgentState
from app.evolution import update_evolution_memory

def generate_node(state: AgentState) -> AgentState:
    """Generate the initial lesson."""

    topic = state["topic"]
    demo_mode = state.get("demo_mode", False)

    lesson = generate_lesson(
        topic=topic,
        demo_mode=demo_mode,
    )

    return {
        **state,
        "current_lesson": lesson.content,
        "current_title": lesson.title,
        "retry_count": 0,
        "rejection_log": [],
    }


def evaluate_node(state: AgentState) -> AgentState:
    """Evaluate the current lesson against the rubric."""

    lesson = state["current_lesson"]

    evaluation = evaluate_lesson(lesson)

    return {
        **state,
        "evaluation": evaluation,
    }


def regenerate_node(state: AgentState) -> AgentState:
    """Regenerate the lesson using evaluator feedback."""

    topic = state["topic"]
    previous_lesson = state["current_lesson"]
    evaluation = state["evaluation"]
    update_evolution_memory(evaluation)

    retry_count = state.get("retry_count", 0) + 1

    rejection_entry = {
        "attempt": retry_count,
        "failed_checks": evaluation.failed_checks,
        "feedback": evaluation.feedback,
        "previous_lesson": previous_lesson,
    }

    rejection_log = state.get("rejection_log", [])
    rejection_log = [*rejection_log, rejection_entry]

    regenerated = generate_lesson(
        topic=topic,
        previous_lesson=previous_lesson,
        feedback=evaluation.feedback,
    )

    return {
        **state,
        "current_lesson": regenerated.content,
        "current_title": regenerated.title,
        "retry_count": retry_count,
        "rejection_log": rejection_log,
    }