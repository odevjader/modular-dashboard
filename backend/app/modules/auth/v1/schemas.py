from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime
from app.models.enums import UserRole

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[str] = None
    role: Optional[str] = None

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: UserRole = UserRole.USER

    @validator("role", pre=True)
    def normalize_role(cls, v):
        """Convert role to lowercase for case-insensitive input."""
        if isinstance(v, str):
            return v.lower()
        return v

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None

    @validator("role", pre=True)
    def normalize_role(cls, v):
        """Convert role to lowercase for case-insensitive input."""
        if isinstance(v, str):
            return v.lower()
        return v

class UserRead(BaseModel):
    id: int
    email: EmailStr
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True