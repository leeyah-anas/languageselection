from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status
from datetime import datetime
from typing import List, Optional, Dict

from .models import UserLanguagePreference
from .schemas import LanguagePreferenceCreate, LanguagePreferenceUpdate
from ...core.constants import NativeLanguage, SupportedLanguage, ProficiencyLevel

class LanguagePreferenceService:
    
    @staticmethod
    def get_language_options() -> Dict:
        """Get all available language options"""
        return {
            "native_languages": [lang.value for lang in NativeLanguage],
            "supported_languages": [lang.value for lang in SupportedLanguage]
        }
    
    @staticmethod
    def create_preference(db: Session, preference: LanguagePreferenceCreate) -> UserLanguagePreference:
        # Check if user already has a preference
        existing = db.query(UserLanguagePreference).filter(
            UserLanguagePreference.user_id == preference.user_id
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Language preference already exists for user {preference.user_id}. Use PUT to update."
            )
        
        db_preference = UserLanguagePreference(
            user_id=preference.user_id,
            native_language=preference.native_language.value,
            supported_language=preference.supported_language.value,
            proficiency_level=preference.proficiency_level.value if preference.proficiency_level else None
        )
        db.add(db_preference)
        db.commit()
        db.refresh(db_preference)
        return db_preference
    
    @staticmethod
    def get_preference_by_user_id(db: Session, user_id: str) -> UserLanguagePreference:
        preference = db.query(UserLanguagePreference).filter(
            UserLanguagePreference.user_id == user_id
        ).first()
        
        if not preference:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No language preference found for user {user_id}"
            )
        return preference
    
    @staticmethod
    def list_preferences(
        db: Session,
        native_language: Optional[str] = None,
        supported_language: Optional[str] = None,
        proficiency_level: Optional[ProficiencyLevel] = None,
        is_active: Optional[bool] = True,
        skip: int = 0,
        limit: int = 100
    ) -> List[UserLanguagePreference]:
        query = db.query(UserLanguagePreference)
        
        if native_language:
            query = query.filter(UserLanguagePreference.native_language == native_language)
        
        if supported_language:
            query = query.filter(UserLanguagePreference.supported_language == supported_language)
        
        if proficiency_level:
            query = query.filter(UserLanguagePreference.proficiency_level == proficiency_level.value)
        
        if is_active is not None:
            query = query.filter(UserLanguagePreference.is_active == is_active)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def update_preference(
        db: Session, 
        user_id: str, 
        preference_update: LanguagePreferenceUpdate
    ) -> UserLanguagePreference:
        preference = db.query(UserLanguagePreference).filter(
            UserLanguagePreference.user_id == user_id
        ).first()
        
        if not preference:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No language preference found for user {user_id}"
            )
        
        # Update fields
        update_data = preference_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            if field in ["native_language", "supported_language"] and value:
                setattr(preference, field, value.value)
            elif field == "proficiency_level" and value:
                setattr(preference, field, value.value)
            else:
                setattr(preference, field, value)
        
        preference.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(preference)
        return preference
    
    @staticmethod
    def delete_preference(db: Session, user_id: str) -> bool:
        preference = db.query(UserLanguagePreference).filter(
            UserLanguagePreference.user_id == user_id
        ).first()
        
        if not preference:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No language preference found for user {user_id}"
            )
        
        db.delete(preference)
        db.commit()
        return True
    
    @staticmethod
    def get_learning_statistics(db: Session) -> dict:
        # Most popular target languages
        target_stats = db.query(
            UserLanguagePreference.supported_language,
            func.count(UserLanguagePreference.id).label('count')
        ).filter(
            UserLanguagePreference.is_active == True
        ).group_by(
            UserLanguagePreference.supported_language
        ).all()
        
        # Most common native languages
        native_stats = db.query(
            UserLanguagePreference.native_language,
            func.count(UserLanguagePreference.id).label('count')
        ).filter(
            UserLanguagePreference.is_active == True
        ).group_by(
            UserLanguagePreference.native_language
        ).all()
        
        # Popular language combinations
        combination_stats = db.query(
            UserLanguagePreference.native_language,
            UserLanguagePreference.supported_language,
            func.count(UserLanguagePreference.id).label('count')
        ).filter(
            UserLanguagePreference.is_active == True
        ).group_by(
            UserLanguagePreference.native_language,
            UserLanguagePreference.supported_language
        ).all()
        
        return {
            "total_active_learners": sum(count for _, count in target_stats),
            "popular_target_languages": [
                {"language": lang, "learner_count": count} 
                for lang, count in target_stats
            ],
            "native_language_breakdown": [
                {"language": lang, "speaker_count": count}
                for lang, count in native_stats
            ],
            "popular_combinations": [
                {
                    "from": native_lang,
                    "to": supported_lang, 
                    "learner_count": count
                }
                for native_lang, supported_lang, count in combination_stats
            ]
        }
