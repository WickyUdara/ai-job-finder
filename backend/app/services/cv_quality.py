import re
import json
from google import genai
from app.core.config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)


def clean_and_parse_json(raw_text: str) -> dict:
    """
    Remove markdown code block markers and escaped underscores from raw Gemini output,
    then parse and return JSON.
    """
    lines = raw_text.strip().splitlines()

    # Remove opening and closing code block lines
    if lines and lines[0].strip().startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]

    cleaned = "\n".join(lines).strip()

    # Replace escaped underscores
    cleaned = re.sub(r'\\_', '_', cleaned)

    print("Final cleaned string for JSON:\n", cleaned)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
        print(f"Failed cleaned string:\n{cleaned}")
        return {"raw": raw_text}



def evaluate_cv_quality(cv_text: str) -> dict:
    """
    Uses Gemini to analyze CV quality:
    Returns a dict with score, rubric breakdown, strengths, improvements, and optional rewrites.
    """
    prompt = (
        "You are an expert ATS resume reviewer. "
        "Analyze this CV text and respond ONLY with valid JSON as specified. "
        "Your JSON MUST include: score (0-100), rubric (ats_readiness, clarity, quantification, keyword_coverage, structure_formatting, consistency, each 0-10), "
        "strengths (list), improvements (list with area, issue, fix_example), rewritten_examples. "
        "DO NOT output any explanations, headings, or markdown—only pure JSON. "
        "Keys are: score, rubric, strengths, improvements, rewritten_examples.\n\n"
        "=== CV Text ===\n"
        f"{cv_text}"
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[prompt]
    )
    print("Gemini LLM raw output:", response.text) 
    return clean_and_parse_json(response.text)
