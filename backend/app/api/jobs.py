from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from bson import ObjectId
from app.db.mongodb import cv_collection
from app.scrapers.glassdoor_selenium import scrape_glassdoor_jobs
from app.services.matching import match_jobs

router = APIRouter()

@router.get("/jobs/search")
def search_jobs(cv_id: str = Query(..., description="Mongo ObjectId of CV"),
                keyword: str = Query(..., description="e.g., 'python developer'"),
                location: Optional[str] = Query(None),
                pages: int = Query(1, ge=1, le=5)):
    # Get CV
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

    # Scrape with Selenium
    jobs = scrape_glassdoor_jobs(keyword=keyword, location=location, pages=pages, headless=True)

    if not jobs:
        return {"matches": [], "total_found": 0}

    matches = match_jobs(cv_text, jobs)
    return {"matches": matches, "total_found": len(matches)}
