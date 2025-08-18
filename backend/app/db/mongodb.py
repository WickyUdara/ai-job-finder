from pymongo import MongoClient
from app.core.config import MONGO_URI, DATABASE_NAME

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

# Collections
cvs = db["cvs"]
jobs = db["jobs"]
