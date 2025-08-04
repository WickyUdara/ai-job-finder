from fastapi import APIRouter, File, UploadFile
from app.db.mongodb import cv_collection
from app.parsers.pdf_parser import extract_text_from_pdf
from app.parsers.docx_parser import extract_text_from_docx
import datetime

router = APIRouter()

@ router.post("/upload_cv/")
async def upload_cv(file: UploadFile = File(...)):
    content = None
    ext = file.filename.split('.')[-1].lower()

    if ext == 'pdf':
        content = extract_text_from_pdf(file.file)
    elif ext in ("docx", "doc"):
        content = extract_text_from_docx(file.file)
    else:
        return {"error": "Unsupported file format. Please upload a PDF or DOCX file."}  
    
    cv_doc = {
        "filename": file.filename,
        "content": content,
        "upload_date": datetime.datetime.now()
    }

    inserted = cv_collection.insert_one(cv_doc)
    return {"cv_id": str(inserted.inserted_id), "content":content}