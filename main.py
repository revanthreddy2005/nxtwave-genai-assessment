import json
from app.output import save_final_outputs
from app.workflow import build_workflow


def main():
    """Run the complete content-generation agent."""

    topic = "Introduction to RAG"

    initial_state = {
        "topic": topic,
        "current_lesson": "",
        "current_title": "",
        "retry_count": 0,
        "max_retries": 2,
        "rejection_log": [],
        "final_lesson": "",
        "final_title": "",
        "demo_mode": False,
    }

    workflow = build_workflow()

    print("=" * 70)
    print("NXTWAVE GENAI CONTENT SYSTEM")
    print("=" * 70)

    print(f"\nTopic: {topic}")
    print("\nStarting agent workflow...\n")

    final_state = workflow.invoke(initial_state)
    save_final_outputs(final_state)

    print("\n" + "=" * 70)
    print("WORKFLOW COMPLETE")
    print("=" * 70)

    print(f"\nFinal title:")
    print(final_state.get("current_title", ""))

    print(f"\nRetry count: {final_state.get('retry_count', 0)}")

    print("\nEvaluation:")
    evaluation = final_state.get("evaluation")

    if evaluation:
        print(evaluation.model_dump_json(indent=2))

    print("\nRejection log:")

    print(
        json.dumps(
            final_state.get("rejection_log", []),
            indent=2,
            ensure_ascii=False,
        )
    )

    print("\nFinal lesson:")
    print("-" * 70)
    print(final_state.get("current_lesson", ""))


if __name__ == "__main__":
    main()