from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.db.mongodb import cv_collection
from bson import ObjectId
import os
from openai import OpenAI

router = APIRouter()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ChatRequest(BaseModel):
    cv_id: str
    question: str

@router.post("/chat/")
async def chat_with_cv(data: ChatRequest):
    try:
        cv_object_id = ObjectId(data.cv_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid CV ID format")

    cv_doc = cv_collection.find_one({"_id": cv_object_id})
    if not cv_doc:
        raise HTTPException(status_code=404, detail="CV not found")

    cv_content = cv_doc.get("content", "")
    if not cv_content:
        raise HTTPException(status_code=404, detail="CV content not found")

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Use the following CV content to answer questions: {cv_content}"},
                {"role": "user", "content": data.question}
            ],
            max_tokens=200,
            temperature=0.5,
        )
        answer = response.choices[0].message.content.strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"answer": answer}
