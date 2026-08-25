from app.state import AgentState


def main():
    state: AgentState = {
        "topic": "Introduction to RAG",
        "current_lesson": "",
        "current_title": "",
        "retry_count": 0,
        "max_retries": 2,
        "rejection_log": [],
        "final_lesson": "",
        "final_title": "",
    }

    print("State initialized successfully.")
    print(state)


if __name__ == "__main__":
    main()