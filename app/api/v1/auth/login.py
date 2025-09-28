from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.domains.auth import schemas
from app.domains.users import models
from app.db.session import get_db
from app.core import security, config
import jwt
from datetime import datetime, timedelta

router = APIRouter()

def create_jwt_token(user_id: int):
    expire = datetime.utcnow() + timedelta(minutes=config.settings.JWT_EXPIRATION_MINUTES)
    payload = {"sub": str(user_id), "exp": expire}
    token = jwt.encode(payload, config.settings.JWT_SECRET_KEY, algorithm=config.settings.JWT_ALGORITHM)
    return token

@router.post("/login")
def login(user_in: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_in.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials.")
    if not security.verify_password(user_in.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials.")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user.")
    if not user.is_verified:
        raise HTTPException(status_code=400, detail="Email not verified.")
    token = create_jwt_token(user.id)
    return {"access_token": token, "token_type": "bearer"}
