from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.db.mongodb import cv_collection
import os
import openai