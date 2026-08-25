import os

from app.evolution import load_evolution_memory
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from app.schemas import LessonOutput


load_dotenv()


def create_llm():
    """Create and return the Gemini language model."""

    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError("GOOGLE_API_KEY was not found in .env")

    return ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        google_api_key=api_key,
    )


def generate_lesson(
    topic: str,
    previous_lesson: str | None = None,
    feedback: list[str] | None = None,
    demo_mode: bool = False,
) -> LessonOutput:
    """
    Generate a beginner-friendly lesson.

    If previous_lesson and feedback are provided, improve the
    previous lesson using the evaluator's feedback.
    """

    llm = create_llm()
    evolution_memory = load_evolution_memory()

    structured_llm = llm.with_structured_output(LessonOutput)

    retry_context = ""
    demo_context = ""
    evolution_context = ""

    # ---------------------------------------------------------
    # EVOLUTION MEMORY
    # ---------------------------------------------------------

    common_failures = evolution_memory.get("common_failures", [])

    if common_failures:
        evolution_context = """
LESSONS LEARNED FROM PREVIOUS EVALUATIONS:

The following recurring mistakes have been detected in
previous generated lessons.

Avoid repeating them:

-------------------
"""

        for failure in common_failures:
            evolution_context += (
                f"- {failure['check_id']} "
                f"({failure['check_name']}): "
                f"{failure['lesson']}\n"
            )

        evolution_context += "-------------------\n"

    # ---------------------------------------------------------
    # DEMONSTRATION MODE
    # ---------------------------------------------------------

    if demo_mode and not previous_lesson:
        demo_context = """
DEMONSTRATION MODE:

This is a controlled evaluation demonstration.

For this FIRST generation only, intentionally include ONE
clear factual error about RAG that the evaluator should be
able to detect.

Use this deliberately incorrect claim:

"RAG guarantees that the AI will always produce a correct answer."

Do not introduce any other deliberate errors.

The purpose is to test whether the evaluator detects the
problem and whether the regeneration step can correct it.
"""

    # ---------------------------------------------------------
    # REGENERATION CONTEXT
    # ---------------------------------------------------------

    if previous_lesson and feedback:
        feedback_text = "\n".join(
            f"- {item}" for item in feedback
        )

        retry_context = f"""
This is a regeneration attempt.

Here is the previous lesson:

-------------------
{previous_lesson}
-------------------

The evaluator rejected the previous lesson.

Evaluator feedback:
{feedback_text}

You MUST fix the problems identified by the evaluator.

Do not blindly rewrite the entire lesson.
Preserve useful explanations and examples when they are
already correct.

Make the smallest meaningful changes needed to address
the evaluator's feedback.
"""

    # ---------------------------------------------------------
    # GENERATION PROMPT
    # ---------------------------------------------------------

    prompt = f"""
You are an expert curriculum engineer creating beginner-friendly
technical learning content.

Your task is to create a lesson about:

TOPIC:
{topic}

TARGET LEARNER:
- A 12th-grade graduate from India.
- Limited English vocabulary.
- Non-English-medium background.
- Has zero prior knowledge of the topic.
- Is beginning an AI career.

LESSON REQUIREMENTS:
1. Explain what the topic means.
2. Explain why it matters.
3. Explain how it works.
4. Use simple English.
5. Introduce technical terms gradually.
6. Explain important technical terms in simple language.
7. Include at least one practical example.
8. Use a clear teaching sequence from simple ideas to more detailed ideas.
9. Do not assume prior knowledge.
10. Avoid unnecessary advanced terminology.
11. Do not make unsupported or technically incorrect claims.
12. Do not use absolute claims such as "always", "guarantees",
    or "ensures" unless they are genuinely justified.

The lesson must be useful as a standalone beginner lesson.

A learner should be able to understand the basic idea after reading it.

{evolution_context}
{demo_context}
{retry_context}

Return only the structured lesson output.
"""

    response = structured_llm.invoke(prompt)

    return response