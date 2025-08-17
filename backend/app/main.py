from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.cv import router as cv_router

app = FastAPI(title="CV Intelligence Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[""], # tighten in later phases
    allow_credentials=True,
    allow_methods=[""],
    allow_headers=["*"],
)

app.include_router(cv_router, prefix="/cv", tags=["cv"])