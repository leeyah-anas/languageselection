from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.domains.users import models
from app.domains.auth import schemas, service
from app.db.session import get_db
import secrets

router = APIRouter()

@router.post("/register", response_model=schemas.UserResponse)
def register_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    if user_in.password != user_in.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match.")
    # Check if user already exists
    user = db.query(models.User).filter(models.User.email == user_in.email).first()
    # | (models.User.username == user_in.username)).first()
    if user:
        raise HTTPException(status_code=400, detail="User with this email already exists.")
    # Create user
    user = service.create_user(db, user_in)

    # Trigger email verification
    verification_token = service.create_verification_token(db, user.id)
    from app.utils.emails import send_verification_email
    send_verification_email(user.email, verification_token.token)

    return user
