from sqlalchemy.orm import Session
from app.db.base import SessionLocal
from app.core.config import settings

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()