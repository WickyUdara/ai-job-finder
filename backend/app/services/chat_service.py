from typing import List, Dict
from google import genai

from app.core.config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

def chat_with_cv(cv_text: str, chat_history: list, user_message: str) -> str:
    # Compose chat context
    system_prompt = (
        "You are an expert CV assistant. Answer the user's questions using ONLY the following CV content. "
        "Be specific and provide only what is present in the CV."
    )
    messages = [{"role": "system", "content": system_prompt},
                {"role": "user", "content": f"CV Content:\n{cv_text}"}]
    # Add previous chat turns (if any)
    for msg in chat_history[-10:]:  # last 10 exchanges
        messages.append(msg)

    messages.append({"role": "user", "content": user_message})

    prompt = "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in messages])
    response = client.models.generate_content(
        model="gemini-1.5-flash-latest",
        contents=[prompt]
    )
    # The text attribute holds the best completion
    return response.text.strip()
