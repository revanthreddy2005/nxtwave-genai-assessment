from pathlib import Path

from app.evaluator import evaluate_lesson
from app.generator import generate_lesson


PROJECT_ROOT = Path(__file__).resolve().parent.parent
LESSON_PATH = PROJECT_ROOT / "outputs" / "test_lesson.txt"


def main():
    with open(LESSON_PATH, "r", encoding="utf-8") as file:
        lesson = file.read()

    print("\nEvaluating Version 1...")

    evaluation = evaluate_lesson(lesson)

    print("\nEvaluation:")
    print(evaluation.model_dump_json(indent=2))

    if evaluation.overall == "PASS":
        print("\nVersion 1 already passed.")
        return

    print("\nVersion 1 failed.")
    print("\nRegenerating using evaluator feedback...")

    regenerated = generate_lesson(
        topic="Introduction to RAG",
        previous_lesson=lesson,
        feedback=evaluation.feedback,
    )

    print("\n" + "=" * 60)
    print("REGENERATED LESSON")
    print("=" * 60)

    print("\nTITLE:")
    print(regenerated.title)

    print("\nLESSON:")
    print(regenerated.content)


if __name__ == "__main__":
    main()