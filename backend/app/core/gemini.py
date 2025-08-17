import os
from app.core.config import GEMINI_API_KEY

def gemini_ocr_pdf_bytes(pdf_bytes: bytes) -> str:
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is not set. Please set it in backend/.env to enable OCR.")
    # TODO: Implement Gemini OCR logic here.
    raise NotImplementedError("Gemini OCR integration not yet implemented. Add SDK calls in core/gemini.py.")
