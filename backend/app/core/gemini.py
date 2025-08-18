import os
from app.core.config import GEMINI_API_KEY

from google import genai
from google.genai import types

# Instantiate Gemini client directly with the API key (no separate config step)
client = genai.Client(api_key=GEMINI_API_KEY)

def gemini_ocr_pdf_bytes(pdf_bytes: bytes) -> str:
    """
    Use Gemini Flash to perform OCR on PDF bytes.
    Returns the extracted text.
    """
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is not set. Please set it in backend/.env to enable OCR.")
    prompt = "Extract all text content from this PDF document using OCR. Return all readable text, even from scanned images."
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash-latest",  # Use your preferred Gemini model name here
            contents=[
                types.Part.from_bytes(data=pdf_bytes, mime_type='application/pdf'),
                prompt
            ]
        )
        return response.text
    except Exception as e:
        raise RuntimeError(f"Gemini OCR failed: {e}")
