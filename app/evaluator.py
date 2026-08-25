import json
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from app.schemas import EvaluationResult


load_dotenv()


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RUBRIC_PATH = PROJECT_ROOT / "data" / "rubric.json"
KNOWLEDGE_BASE_PATH = PROJECT_ROOT / "data" / "knowledge_base.md"

def create_llm():
    """Create and return the Gemini language model."""

    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError("GOOGLE_API_KEY was not found in .env")

    return ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        google_api_key=api_key,
    )


def load_rubric() -> dict:
    """Load the evaluation rubric from the JSON file."""

    with open(RUBRIC_PATH, "r", encoding="utf-8") as file:
        return json.load(file)
    
def load_knowledge_base() -> str:
    """Load the trusted RAG knowledge base."""

    with open(KNOWLEDGE_BASE_PATH, "r", encoding="utf-8") as file:
        return file.read()


def evaluate_lesson(lesson: str) -> EvaluationResult:
    """Evaluate a generated lesson against the project rubric."""

    rubric = load_rubric()
    knowledge_base = load_knowledge_base()
    llm = create_llm()
    
    

    structured_llm = llm.with_structured_output(EvaluationResult)

    prompt = f"""
You are a strict curriculum quality evaluator.

Your job is to evaluate a beginner lesson about:
Introduction to RAG

TARGET LEARNER:
- 12th-grade graduate from India
- Limited English vocabulary
- Non-English-medium background
- Zero prior knowledge of RAG

IMPORTANT EVALUATION RULES:

1. Evaluate the lesson against EVERY rubric checkpoint.
2. Every checkpoint must be either PASS or FAIL.
3. Never give partial credit.
4. Do not assume missing information is present.
5. Be strict about technical accuracy.
6. Identify misleading, exaggerated, or absolute technical claims.
7. Check whether important technical terms are explained.
8. Check whether the lesson actually teaches the topic rather than
   simply mentioning concepts.
9. If a checkpoint fails, explain exactly why.
10. Give actionable feedback that another generation step can use
    to improve the lesson.
11. The overall result must be FAIL if ANY checkpoint fails.
12. The overall result can be PASS only when ALL checkpoints pass.

RUBRIC:
{json.dumps(rubric, indent=2)}

TRUSTED KNOWLEDGE BASE:
Use this knowledge base as the primary factual reference when
evaluating the lesson's important technical claims.

-------------------
{knowledge_base}
-------------------

GROUNDING RULE:
For R7, use the trusted knowledge base as the primary factual
reference.

Do not mark a claim as FAIL merely because the knowledge base
does not explicitly mention it.

Mark R7 as FAIL when an important factual claim:
- directly contradicts the trusted knowledge base,
- materially changes the meaning of information in the knowledge base,
- or makes a strong factual claim that cannot reasonably be
  supported by the available knowledge.

Distinguish between:
- "not mentioned in the knowledge base"
and
- "contradicted or materially unsupported by the knowledge base."

Do not require every sentence of the lesson to appear in the
knowledge base.

LESSON TO EVALUATE:
-------------------
{lesson}
-------------------

Return the evaluation using the required structured format.

For every checkpoint:
- use its exact rubric ID
- use its exact rubric name
- return PASS or FAIL
- provide a concise but specific reason

For failed checkpoints, provide actionable feedback.
For passed checkpoints, briefly explain why they passed.
"""

    result = structured_llm.invoke(prompt)

    return result