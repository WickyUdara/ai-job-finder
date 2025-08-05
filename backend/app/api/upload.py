from fastapi import APIRouter, UploadFile, File
from app.db.mongodb import cv_collection
from app.parsers.pdf_parser import extract_text_from_pdf
from app.parsers.docx_parser import extract_text_from_docx
import datetime

router = APIRouter()

@router.post("/upload-cv/")
async def upload_cv(file: UploadFile = File(...)):
    content = None
    ext = file.filename.lower().split('.')[-1]

    if ext == "pdf":
        content = extract_text_from_pdf(file.file)
    elif ext in ("docx", "doc"):
        content = extract_text_from_docx(file.file)
    else:
        return {"error": "File type not supported"}

    cv_doc = {
        "filename": file.filename,
        "content": content,
        "created_at": datetime.datetime.utcnow()
    }
    inserted = cv_collection.insert_one(cv_doc)
    return {"cv_id": str(inserted.inserted_id), "content": content}
