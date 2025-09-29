from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List
from app.core.constants import NativeLanguage, SupportedLanguage, ProficiencyLevel, DailyLearningGoal,LearningReason

class LanguageOptionsResponse(BaseModel):
    """Available language options for selection"""
    native_languages: List[str] = Field(..., description="Languages user can speak")
    supported_languages: List[str] = Field(..., description="Languages user can learn")

class LanguagePreferenceCreate(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=100, description="Unique user identifier")
    native_language: NativeLanguage = Field(..., description="Language the user speaks")
    supported_language: SupportedLanguage = Field(..., description="Language the user wants to learn")
    proficiency_level: Optional[ProficiencyLevel] = Field(None, description="Current proficiency level in target language")
    learning_reason: Optional[LearningReason] = Field(..., description= "Reason for learning")
    daily_goal:Optional [DailyLearningGoal] = Field(..., description= "Daily learning time")

class LanguagePreferenceUpdate(BaseModel):
    native_language: Optional[NativeLanguage] = Field(None, description="Language the user speaks")
    Supported_language: Optional[SupportedLanguage] = Field(None, description="Language the user wants to learn")
    proficiency_level: Optional[ProficiencyLevel] = Field(None, description="Current proficiency level")
    learning_reason: Optional[LearningReason] = Field(None, description="Reason for learning (travel, career, culture, other)")
    daily_goal: Optional[DailyLearningGoal] = Field(None, description="Daily learning time goal (light: 5min, steady: 10min, intense: 20min)")
    is_active: Optional[bool] = Field(None, description="Whether this preference is active")
    

class LanguagePreferenceResponse(BaseModel):
    id: int
    user_id: str
    native_language: str
    supported_language: str
    proficiency_level: Optional[str]
    learning_reason: Optional[str]
    daily_goal: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True