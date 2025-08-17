from fastapi import APIRouter, UploadFile, File, HTTPException
from bson import ObjectId
from datetime import datetime
from app.db.mongodb import cvs
from app.db.schemas import CVUploadResponse, CVBasicInfo
from app.services.cv_extraction import extract_text_from_pdf, extract_text_from_docx

router = APIRouter()

@router.post("/upload", response_model=CVUploadResponse)
async def upload_cv(file: UploadFile = File(...)):
    filename = file.filename
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty file upload")

    ext = (filename or "").split(".")[-1].lower()
    if ext == "pdf":
        text, ocr_used = extract_text_from_pdf(content)
    elif ext == "docx":
        text, ocr_used = extract_text_from_docx(content)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type. Use PDF or DOCX.")

    if not text or len(text.strip()) == 0:
        raise HTTPException(status_code=422, detail="Could not extract any text from the file.")

    doc = {
        "filename": filename,
        "raw_text": text,
        "ocr_used": ocr_used,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    res = cvs.insert_one(doc)
    return CVUploadResponse(cv_id=str(res.inserted_id), filename=filename, ocr_used=ocr_used)

@router.get("/{cv_id}", response_model=CVBasicInfo)
async def get_cv(cv_id: str):
    try:
        oid = ObjectId(cv_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid CV ID")

    doc = cvs.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="CV not found")

    raw = (doc.get("raw_text") or "").strip()
    preview = raw[:2000]
    return CVBasicInfo(
        cv_id=cv_id,
        filename=doc.get("filename", ""),
        ocr_used=bool(doc.get("ocr_used", False)),
        raw_text_preview=preview
    )
