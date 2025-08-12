import sys, asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import upload, chatbot
from app.api import jobs_arbeitnow

if sys.platform.startswith("win"):
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    except Exception:
        pass

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router)
app.include_router(chatbot.router)
app.include_router(jobs_arbeitnow.router)
