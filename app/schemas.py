from typing import List, Literal

from pydantic import BaseModel, Field


class EvaluationCheck(BaseModel):
    """Result of one rubric checkpoint."""

    id: str
    name: str
    result: Literal["PASS", "FAIL"]
    reason: str


class EvaluationResult(BaseModel):
    """Structured result produced by the evaluator."""

    overall: Literal["PASS", "FAIL"]
    checks: List[EvaluationCheck]
    failed_checks: List[str] = Field(default_factory=list)
    feedback: List[str] = Field(default_factory=list)


class LessonOutput(BaseModel):
    """A generated beginner-friendly lesson."""

    title: str
    content: str

