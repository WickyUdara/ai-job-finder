from fastapi import APIRouter, HTTPException
from bson import ObjectId
from app.db.mongodb import cvs
from app.services.cv_quality import evaluate_cv_quality
from datetime import datetime

router = APIRouter()

@router.post("/{cv_id}/quality/evaluate")
async def evaluate_cv_quality_api(cv_id: str):
    try:
        oid = ObjectId(cv_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid CV ID")

    doc = cvs.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="CV not found")
    cv_text = doc.get("raw_text", "")
    if not cv_text:
        raise HTTPException(status_code=404, detail="CV text not found")

    result = evaluate_cv_quality(cv_text)
    result['evaluated_at'] = datetime.utcnow()
    cvs.update_one({"_id": oid}, {"$set": {"quality_report": result, "updated_at": datetime.utcnow()}})
    return result

@router.get("/{cv_id}/quality")
async def get_cv_quality_api(cv_id: str):
    try:
        oid = ObjectId(cv_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid CV ID")

    doc = cvs.find_one({"_id": oid})
    if not doc or "quality_report" not in doc:
        raise HTTPException(status_code=404, detail="Quality report not found")
    return doc["quality_report"]
