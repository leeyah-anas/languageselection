from fastapi import APIRouter, Depends, status, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional

from ...db.session import get_db
from ...domains.languages.schemas import (
    LanguagePreferenceCreate, 
    LanguagePreferenceUpdate, 
    LanguagePreferenceResponse,
    LanguageOptionsResponse,
)
from ...domains.languages.services import LanguagePreferenceService
from ...core.constants import ProficiencyLevel, LearningReason, DailyLearningGoal

router = APIRouter(prefix="/languages", tags=["Language Learning Preferences"])

@router.get("/options", response_model=LanguageOptionsResponse)
async def get_language_options():
    return LanguagePreferenceService.get_language_options()

@router.post("/preferences", response_model=LanguagePreferenceResponse, status_code=status.HTTP_201_CREATED)
async def create_language_preference(
    preference: LanguagePreferenceCreate,
    db: Session = Depends(get_db)
):
    return LanguagePreferenceService.create_preference(db, preference)

@router.get("/preferences/{user_id}", response_model=LanguagePreferenceResponse)
async def get_language_preference(user_id: str, db: Session = Depends(get_db)):
    return LanguagePreferenceService.get_preference_by_user_id(db, user_id)

@router.get("/preferences", response_model=List[LanguagePreferenceResponse])
async def list_language_preferences(
    native_language: Optional[str] = Query(None, description="Filter by native language"),
    supported_language: Optional[str] = Query(None, description="Filter by target language"),
    proficiency_level: Optional[ProficiencyLevel] = Query(None, description="Filter by proficiency level"),
    learning_reason: Optional[LearningReason] = Query(None, description="Filter by learning reason"),
    daily_goal: Optional[DailyLearningGoal] = Query(None, description="Filter by daily goal"),                                                 
    is_active: Optional[bool] = Query(True, description="Filter by active status"),
    skip: int = Query(0, ge=0, description="Skip records for pagination"),
    limit: int = Query(100, ge=1, le=1000, description="Limit records for pagination"),
    db: Session = Depends(get_db)
):
    return LanguagePreferenceService.list_preferences(
        db, native_language, supported_language, proficiency_level, learning_reason, daily_goal, is_active, skip, limit
    )

@router.put("/preferences/{user_id}", response_model=LanguagePreferenceResponse)
async def update_language_preference(
    user_id: str,
    preference_update: LanguagePreferenceUpdate,
    db: Session = Depends(get_db)
):
    """Update language preference for a specific user"""
    return LanguagePreferenceService.update_preference(db, user_id, preference_update)

@router.delete("/preferences/{user_id}")
async def delete_language_preference(user_id: str, db: Session = Depends(get_db)):
    """Delete language preference for a specific user"""
    LanguagePreferenceService.delete_preference(db, user_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": f"Language preference deleted for user {user_id}"}
    )

@router.get("/stats")
async def get_learning_statistics(db: Session = Depends(get_db)):
    return LanguagePreferenceService.get_learning_statistics(db)
