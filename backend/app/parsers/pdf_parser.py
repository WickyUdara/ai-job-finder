import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Make sure .env is loaded
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

# GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# if not GEMINI_API_KEY:
#     raise ValueError('GEMINI_API_KEY not found in environment variables. Please set it in your .env file.')

client = genai.Client()

def extract_text_from_pdf(file_data):
    """Extract text from a PDF using Gemini API (with OCR for scanned PDFs)."""
    file_data.seek(0)
    pdf_bytes = file_data.read()
    prompt = "Extract all text content from the provided PDF document."

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            types.Part.from_bytes(
                data=pdf_bytes,
                mime_type='application/pdf'
            ),
            prompt
        ]
    )
    return response.text
