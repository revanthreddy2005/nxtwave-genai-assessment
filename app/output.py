import json
from pathlib import Path

from app.state import AgentState


PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "outputs"


def save_final_outputs(state: AgentState) -> None:
    """Save the final lesson, evaluation, and rejection log."""

    OUTPUT_DIR.mkdir(exist_ok=True)

    title = state.get("current_title", "Introduction to RAG")
    lesson = state.get("current_lesson", "")
    evaluation = state.get("evaluation")
    rejection_log = state.get("rejection_log", [])

    # Save final lesson.
    final_lesson_path = OUTPUT_DIR / "final_lesson.md"

    with open(final_lesson_path, "w", encoding="utf-8") as file:
        file.write(f"# {title}\n\n")
        file.write(lesson)

    # Save evaluation.
    evaluation_path = OUTPUT_DIR / "evaluation.json"

    if evaluation:
        with open(evaluation_path, "w", encoding="utf-8") as file:
            json.dump(
                evaluation.model_dump(),
                file,
                indent=2,
                ensure_ascii=False,
            )

    # Save rejection log.
    rejection_log_path = OUTPUT_DIR / "rejection_log.json"

    with open(rejection_log_path, "w", encoding="utf-8") as file:
        json.dump(
            rejection_log,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print("\nOutputs saved:")
    print(f"- {final_lesson_path}")
    print(f"- {evaluation_path}")
    print(f"- {rejection_log_path}")