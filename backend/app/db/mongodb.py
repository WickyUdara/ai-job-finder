from pymongo import MongoClient
import os

# For local dev, set fallback URI here or use .env
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")

client = MongoClient(MONGO_URI)
db = client["job_finder"]
cv_collection = db["cvs"]
jobs_collection = db["jobs"]  
