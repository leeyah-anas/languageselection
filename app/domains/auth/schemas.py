from pydantic import BaseModel, EmailStr, constr
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr
    language_spoken: str
    language_learning: str
    daily_goal: str
    learning_reason: str

class UserCreate(UserBase):
    password: constr(min_length=8)
    confirm_password: constr(min_length=8)

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_verified: bool

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str
