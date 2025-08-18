from fastapi import APIRouter, HTTPException
from app.db.mongodb import cvs
from bson import ObjectId
from app.services.cv_structuring import extract_structured_fields

router = APIRouter()

@router.post("/{cv_id}/structure")
async def structure_cv(cv_id: str):
    try:
        oid = ObjectId(cv_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid CV ID")

    doc = cvs.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="CV not found")

    cv_text = doc.get("raw_text", "")
    if not cv_text:
        raise HTTPException(status_code=404, detail="CV content not found")

    fields = extract_structured_fields(cv_text)
    cvs.update_one({"_id": oid}, {"$set": {"extracted_fields": fields}})
    return fields
