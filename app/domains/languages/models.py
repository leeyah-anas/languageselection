from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from ...db.base import Base


class UserLanguagePreference(Base):
    __tablename__ = "user_language_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True, nullable=False)
    native_language = Column(String, nullable=False)  
    supported_language = Column(String, nullable=False)  
    proficiency_level = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
