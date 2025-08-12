from typing import List, Dict, Tuple
import re

def extract_skills_from_cv(cv_text: str) -> List[str]:
    seed_skills = [
        "python", "fastapi", "mongodb", "nlp", "machine learning", "ml",
        "data science", "aws", "docker", "kubernetes", "react", "sql",
        "pandas", "numpy", "spacy", "selenium", "beautifulsoup", "llm",
        "openai", "huggingface", "streamlit", "playwright", "azure", "gcp",
        "rest", "graphql", "microservices", "airflow", "spark"
    ]
    text = cv_text.lower()
    found = set()
    for s in seed_skills:
        if re.search(rf"\b{re.escape(s)}\b", text):
            found.add(s)
    return list(found)

def score_job_against_skills(job: Dict, skills: List[str]) -> Tuple[int, List[str]]:
    desc_blob = (job.get("title","") + " " + job.get("company","") + " " + job.get("description","") + " " + " ".join(job.get("tags", []))).lower()
    matched = [sk for sk in skills if sk in desc_blob]
    return len(matched), matched

def match_jobs(cv_text: str, jobs: List[Dict]) -> List[Dict]:
    skills = extract_skills_from_cv(cv_text)
    scored = []
    for job in jobs:
        score, matched = score_job_against_skills(job, skills)
        if score > 0:
            j = dict(job)
            j["score"] = score
            j["matched_skills"] = matched
            scored.append(j)
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored
