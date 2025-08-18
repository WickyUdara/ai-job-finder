from app.db.mongodb import cvs, jobs
from scipy.spatial import distance

def get_cv_embedding(cv_id):
    doc = cvs.find_one({"_id": cv_id})
    return doc.get("embedding")  # You must run CV embedding similarly as jobs

def match_cv_to_jobs(cv_id, top_k=5):
    cv_embedding = get_cv_embedding(cv_id)
    if not cv_embedding:
        return []
    job_scores = []
    for job in jobs.find({"embedding": {"$exists": True}}):
        score = 1 - distance.cosine(cv_embedding, job["embedding"])
        job_scores.append({
            "job_id": str(job["_id"]),
            "title": job["title"],
            "score": float(score)
        })
    job_scores.sort(key=lambda x: -x["score"])
    return job_scores[:top_k]
