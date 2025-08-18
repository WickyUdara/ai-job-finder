from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.cv import router as cv_router
from app.api.structure import router as structure_router
from app.api.chat import router as chat_router
from app.api.quality import router as quality_router

app = FastAPI(title="CV Intelligence Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[""], # tighten in later phases
    allow_credentials=True,
    allow_methods=[""],
    allow_headers=["*"],
)

app.include_router(cv_router, prefix="/cv", tags=["cv"])
app.include_router(structure_router, prefix="/cv", tags=["structure"])
app.include_router(chat_router, prefix="/cv", tags=["chat"])
app.include_router(quality_router, prefix="/cv", tags=["quality"])
