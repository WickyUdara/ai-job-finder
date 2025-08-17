from google import genai
from app.core.config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

def extract_structured_fields(cv_text: str) -> dict:
    prompt = (
        "Extract the following fields from this CV in strict JSON format:\n"
        "name, contact (email, phone, location), summary, experience (company, role, start, end, bullets[]), "
        "education (school, degree, start, end), skills (programming, ml, data, cloud, other), certifications, years_experience. "
        "Do not add fields not present."
    )
    response = client.models.generate_content(
        model="gemini-1.5-flash-latest",
        contents=[cv_text, prompt]
    )
    # Parse Gemini's output as JSON
    import json
    try:
        structured_fields = json.loads(response.text)
    except Exception:
        structured_fields = {"raw": response.text}
    return structured_fields
