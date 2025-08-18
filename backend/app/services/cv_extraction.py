import io
import pdfplumber
import docx
from typing import Tuple
from app.core.gemini import gemini_ocr_pdf_bytes

MIN_EXTRACTED_LEN = 200  # heuristic threshold for OCR fallback

def extract_text_from_pdf(file_bytes: bytes) -> Tuple[str, bool]:
    text = ""
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            pages = []
            for page in pdf.pages:
                pt = page.extract_text() or ""
                pages.append(pt)
            text = "\n".join(pages).strip()
    except Exception:
        text = ""

    if len(text) >= MIN_EXTRACTED_LEN:
        return text, False

    try:
        ocr_text = gemini_ocr_pdf_bytes(file_bytes)
        if ocr_text and len(ocr_text.strip()) > 0:
            return ocr_text.strip(), True
    except Exception:
        pass

    return text, False

def extract_text_from_docx(file_bytes: bytes) -> Tuple[str, bool]:
    f = io.BytesIO(file_bytes)
    document = docx.Document(f)
    lines = [p.text for p in document.paragraphs if p.text]
    text = "\n".join(lines).strip()
    return text, False
