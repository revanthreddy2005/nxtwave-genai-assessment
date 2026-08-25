from app.workflow import build_workflow


def main():
    workflow = build_workflow()

    print("LangGraph workflow compiled successfully.")
    print(workflow)


if __name__ == "__main__":
    main()