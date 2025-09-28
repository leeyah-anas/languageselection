from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.domains.auth import service
from app.domains.users import models
from app.db.session import get_db
from app.utils.emails import send_verification_email

router = APIRouter()

@router.post("/send-verification")
def send_verification(email: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    if user.is_verified:
        raise HTTPException(status_code=400, detail="User already verified.")

    # Create verification token in database
    verification_token = service.create_verification_token(db, user.id)
    send_verification_email(user.email, verification_token.token)
    return {"msg": "Verification email sent."}

@router.get("/verify", include_in_schema=False)
def verify_email(token: str, db: Session = Depends(get_db)):
    # Get token from database
    verification_token = service.get_verification_token(db, token)
    if not verification_token:
        raise HTTPException(status_code=400, detail="Invalid or expired token.")

    # Mark user as verified
    user = db.query(models.User).filter(models.User.id == verification_token.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    user.is_verified = True
    service.mark_token_as_used(db, verification_token.id)
    db.commit()

    return {"msg": "Email verified successfully."}
