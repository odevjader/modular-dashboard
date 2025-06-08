# backend/app/core_modules/auth/v1/schemas.py
from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List # Changed to List, or use list directly if Python >= 3.9
from datetime import datetime
from app.models.enums import UserRole

# New UserBase schema
class UserBase(BaseModel):
    email: EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[str] = None
    role: Optional[str] = None

class UserCreate(UserBase): # Inherit from UserBase
    password: str
    role: UserRole = UserRole.USER
    is_active: bool = True # Add is_active field

    @validator("role", pre=True) # Keep existing validator
    def normalize_role(cls, v):
        """Convert role to lowercase for case-insensitive input."""
        if isinstance(v, str):
            return v.lower()
        return v

class UserUpdate(BaseModel): # UserUpdate can also inherit from UserBase if appropriate, but not specified
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

class UserResponse(BaseModel): # Renamed from UserRead
    id: int
    email: EmailStr # Kept as UserBase only has email, UserResponse includes more
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# New UserListResponse schema
class UserListResponse(BaseModel):
    items: List[UserResponse] # Use the renamed UserResponse and imported List
    total: int
    page: int
    size: int
    pages: int # Total number of pages