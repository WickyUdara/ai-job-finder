from fastapi import APIRouter, HTTPException, Body
from app.db.mongodb import cvs
from bson import ObjectId
from app.services.chat_service import chat_with_cv

router = APIRouter()

@router.post("/{cv_id}/chat")
async def chat_with_cv_api(
    cv_id: str,
    message: str = Body(..., embed=True)
):
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

    chat_history = doc.get("chat_history", [])

    reply = chat_with_cv(cv_text, chat_history, message)

    # Save chat to history
    new_msg = {"role": "user", "content": message}
    new_reply = {"role": "assistant", "content": reply}
    new_history = chat_history + [new_msg, new_reply]

    cvs.update_one({"_id": oid}, {"$set": {"chat_history": new_history}})

    return {
        "reply": reply,
        "messages": new_history
    }
