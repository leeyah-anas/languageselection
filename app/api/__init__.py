# File: app/api/__init__.py
from fastapi import APIRouter
from app.api.v1.languages import router as language_router  # Add 'app.' prefix

api_router = APIRouter()
api_router.include_router(language_router)