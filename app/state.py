from typing import TypedDict

from app.schemas import EvaluationResult


class AgentState(TypedDict, total=False):
    """State carried through the content-generation workflow."""

    topic: str
    current_lesson: str
    current_title: str

    evaluation: EvaluationResult

    retry_count: int
    max_retries: int

    rejection_log: list[dict]

    final_lesson: str
    final_title: str
    demo_mode: bool

