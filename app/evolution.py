import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
MEMORY_PATH = PROJECT_ROOT / "data" / "evolution_memory.json"


def load_evolution_memory() -> dict:
    """Load persistent lessons learned from previous failures."""

    if not MEMORY_PATH.exists():
        return {"common_failures": []}

    with open(MEMORY_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def save_evolution_memory(memory: dict) -> None:
    """Save persistent evolution memory."""

    with open(MEMORY_PATH, "w", encoding="utf-8") as file:
        json.dump(
            memory,
            file,
            indent=2,
            ensure_ascii=False,
        )


def update_evolution_memory(evaluation) -> None:
    """
    Store reusable lessons from failed evaluations.
    """

    if evaluation.overall == "PASS":
        return

    memory = load_evolution_memory()

    existing = memory.get("common_failures", [])

    for check_id in evaluation.failed_checks:

        check = next(
            (
                item
                for item in evaluation.checks
                if item.id == check_id
            ),
            None,
        )

        if not check:
            continue

        failure = {
            "check_id": check.id,
            "check_name": check.name,
            "lesson": check.reason,
        }

        # Avoid storing the exact same failure repeatedly.
        already_exists = any(
            item["check_id"] == failure["check_id"]
            and item["lesson"] == failure["lesson"]
            for item in existing
        )

        if not already_exists:
            existing.append(failure)

    memory["common_failures"] = existing

    save_evolution_memory(memory)