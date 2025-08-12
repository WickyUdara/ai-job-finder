from fastapi import APIRouter, HTTPException, Query
from app.services.matching import match_jobs, extract_skills_from_cv
from app.services.arbeitnow_fetcher import fetch_arbeitnow_jobs


router = APIRouter()

@router.get("/jobs/arbeitnow")
def jobs_from_arbeitnow(
    cv_id: str = Query(..., description="Mongo ObjectId of CV"),
    pages: int = Query(1, ge=1, le=5),
):
    # Load CV
    try:
        obj_id = ObjectId(cv_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid CV ID")

    cv = cv_collection.find_one({"_id": obj_id})
    if not cv:
        raise HTTPException(status_code=404, detail="CV not found")

    cv_text = cv.get("content", "")
    if not cv_text:
        raise HTTPException(status_code=404, detail="CV content not found")

    # Extract skills from CV to form the query
    skills = extract_skills_from_cv(cv_text)
    query_str = " ".join(skills[:5])  # limit to top-N skills to keep search short

    # Fetch jobs from Arbeitnow
    jobs = fetch_arbeitnow_jobs(query=query_str, limit_pages=pages)

    if not jobs:
        return {"matches": [], "total_found": 0}

    # Match jobs
    matches = match_jobs(cv_text, jobs)
    return {"matches": matches, "total_found": len(matches)}
