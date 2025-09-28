from sqlalchemy.orm import Session
from app.domains.auth import schemas
from app.domains.users import models
from app.core import security
from datetime import datetime, timedelta
import secrets


def create_user(db: Session, user_in: schemas.UserCreate) -> models.User:
    hashed_password = security.get_password_hash(user_in.password)
    db_user = models.User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hashed_password,
        language_spoken=user_in.language_spoken,
        language_learning=user_in.language_learning,
        daily_goal=user_in.daily_goal,
        learning_reason=user_in.learning_reason,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_verification_token(db: Session, user_id: int) -> models.VerificationToken:
    token = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(hours=24)  # 24 hour expiration

    db_token = models.VerificationToken(
        user_id=user_id,
        token=token,
        expires_at=expires_at
    )
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token


def get_verification_token(db: Session, token: str) -> models.VerificationToken:
    return db.query(models.VerificationToken).filter(
        models.VerificationToken.token == token,
        models.VerificationToken.is_used == False,
        models.VerificationToken.expires_at > datetime.utcnow()
    ).first()


def mark_token_as_used(db: Session, token_id: int):
    db_token = db.query(models.VerificationToken).filter(models.VerificationToken.id == token_id).first()
    if db_token:
        db_token.is_used = True
        db.commit()
