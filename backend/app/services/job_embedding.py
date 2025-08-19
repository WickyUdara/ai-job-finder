from google import genai
from app.core.config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

def embed_job_text(title, desc, requirements, skills):
    text = f"Title: {title}\nDescription: {desc}\nRequirements: {','.join(requirements)}\nSkills: {','.join(skills)}"
    response = client.models.embed_content(
        model="models/text-embedding-004",
        contents=[text]
    )
    return response.embeddings[0].values   

    
