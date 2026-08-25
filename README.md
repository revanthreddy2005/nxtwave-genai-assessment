# NxtWave GenAI Content Systems Agent

An agentic GenAI content generation and evaluation system built for the NxtWave GenAI Engineer assessment.

The system generates beginner-friendly technical lessons, evaluates them against a structured quality rubric and trusted knowledge base, and automatically regenerates rejected lessons using evaluator feedback.

## Overview

The system is designed around a Generate → Evaluate → Regenerate workflow.

Given a topic such as `Introduction to RAG`, the system:

1. Generates a beginner-friendly lesson.
2. Evaluates the lesson against seven quality criteria.
3. Checks important factual claims against a trusted knowledge base.
4. If the lesson passes all checks, the workflow finishes.
5. If any check fails, the evaluator provides actionable feedback.
6. The system regenerates the lesson using the previous lesson and feedback.
7. The regenerated lesson is evaluated again.
8. Rejection history is stored for auditing.
9. Reusable lessons from failures are stored in persistent evolution memory.

## Architecture

```text
                    Topic
                      |
                      v
                +-----------+
                | Generator |
                +-----------+
                      |
                      v
                   Lesson
                      |
                      v
                +-----------+
                | Evaluator |
                +-----------+
                      |
                PASS / FAIL
                  /       \
               PASS       FAIL
                |           |
                v           v
               END      Regenerate
                            |
                            v
                       Evaluator

## Evaluation Rubric

The evaluator checks the generated lesson against:

R1 - Accuracy
R2 - Beginner Friendly
R3 - Key Concepts
R4 - Example
R5 - Jargon Control
R6 - Teaching Flow
R7 - Grounding

Every checkpoint receives either PASS or FAIL.

The overall evaluation is PASS only when all checkpoints pass.

## Grounding

Important technical claims are checked against this knowledge base rather than relying only on general model knowledge.

This helps detect unsupported or contradictory claims.

Self-Evolution

The system maintains persistent evolution memory in:

data/evolution_memory.json

When an evaluation fails, reusable lessons from the failure can be stored.

For example, during testing the evaluator detected that claiming:

"RAG guarantees that the AI will always produce a correct answer."

was incorrect.

The system stored this failure under Accuracy and Grounding so that future generations can avoid repeating the same type of mistake.

Demonstrated Agentic Loop

The system was tested using a controlled deliberate error.

Version 1

The generated lesson intentionally contained an incorrect absolute claim about RAG accuracy.

The evaluator detected:

R1 - Accuracy: FAIL
R7 - Grounding: FAIL

The evaluator then produced actionable feedback explaining that RAG does not guarantee completely correct answers.

Version 2

The regeneration step used the previous lesson and evaluator feedback to correct the problem.

The regenerated lesson passed:

R1 - PASS
R2 - PASS
R3 - PASS
R4 - PASS
R5 - PASS
R6 - PASS
R7 - PASS

The final result was:

OVERALL: PASS
Project Structure
nxtwave-genai-assessment/
|
├── app/
│   ├── __init__.py
│   ├── evaluator.py
│   ├── evolution.py
│   ├── generator.py
│   ├── nodes.py
│   ├── output.py
│   ├── schemas.py
│   ├── state.py
│   └── workflow.py
|
├── data/
│   ├── evolution_memory.json
│   ├── knowledge_base.md
│   └── rubric.json
|
├── outputs/
│   ├── evaluation.json
│   ├── final_lesson.md
│   ├── rejection_log.json
│   ├── test_lesson.txt
│   └── test_lesson_v2.txt
|
├── tests/
│   ├── evaluate_v2.py
│   ├── manual_evaluator_test.py
│   ├── manual_regeneration_test.py
│   ├── test_evolution.py
│   ├── test_state.py
│   └── test_workflow.py
|
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
Requirements
Python 3.11+
Google Gemini API key
Dependencies listed in requirements.txt
Setup

Create a virtual environment:

python -m venv .venv

Activate it on Windows PowerShell:

.\.venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt

Create a .env file in the project root:

GOOGLE_API_KEY=your_api_key_here

The .env file is excluded from Git using .gitignore.

Running the Agent

Run:

python main.py

The workflow generates and evaluates the lesson.

Successful outputs are saved in:

outputs/

including:

final_lesson.md
evaluation.json
rejection_log.json
Technologies
Python
LangChain
LangGraph
Google Gemini
Pydantic
JSON
Markdown
Key Design Decisions
Structured Evaluation

The evaluator returns a structured evaluation instead of unstructured feedback. This makes the PASS/FAIL decision machine-readable and allows the workflow to make routing decisions.

Conditional Regeneration

The workflow only regenerates content when evaluation fails.

Retry Limit

A maximum retry count prevents the workflow from entering an infinite regeneration loop.

Persistent Rejection History

Rejected attempts and evaluator feedback are stored so the improvement process can be inspected later.

Evolution Memory

Reusable lessons from previous failures are persisted and provided to future generation attempts.

Example Output

Final evaluation:

{
  "overall": "PASS"
}

The complete evaluation and rejection history are available in the outputs/ directory.

Assessment Demonstration

The project includes a controlled demonstration showing:

Deliberate Error
      |
      v
Evaluator detects failure
      |
      v
Actionable feedback
      |
      v
Regeneration
      |
      v
All rubric checks PASS