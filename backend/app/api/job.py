from fastapi import APIRouter, HTTPException, Body
from app.db.mongodb import db
from app.services.job_embedding import embed_job_text
from app.services.job_matching import match_cv_to_jobs


jobs = db["jobs"]
router = APIRouter()

@router.post("/upload")
async def upload_job(data: dict = Body(...)):
    title = data.get("title")
    desc = data.get("description")
    requirements = data.get("requirements", [])
    skills = data.get("skills", [])
    employer = data.get("employer")
    location = data.get("location")
    if not title or not desc:
        raise HTTPException(status_code=400, detail="Job title and description required.")
    embedding = embed_job_text(title, desc, requirements, skills)
    job_doc = {
        "title": title,
        "description": desc,
        "requirements": requirements,
        "skills": skills,
        "employer": employer,
        "location": location,
        "embedding": embedding,
    }
    result = jobs.insert_one(job_doc)
    job_doc["job_id"] = str(result.inserted_id)
    return job_doc

@router.get("/list")
async def list_jobs():
    job_list = []
    for job in jobs.find({}):
        job["job_id"] = str(job["_id"])
        job.pop("_id")
        job_list.append(job)
    return job_list


@router.get("/match/{cv_id}")
async def match_jobs_endpoint(cv_id: str):
    results = match_cv_to_jobs(cv_id)
    return results

