from pathlib import Path

from app.evaluator import evaluate_lesson


PROJECT_ROOT = Path(__file__).resolve().parent.parent
LESSON_PATH = PROJECT_ROOT / "outputs" / "test_lesson_v2.txt"


def main():
    with open(LESSON_PATH, "r", encoding="utf-8") as file:
        lesson = file.read()

    print("\nEvaluating Version 2...")

    result = evaluate_lesson(lesson)

    print("\n" + "=" * 60)
    print("VERSION 2 EVALUATION")
    print("=" * 60)

    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()