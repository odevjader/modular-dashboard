# backend/app/core_modules/auth/v1/schemas.py
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
from app.models.enums import UserRole

# UserBase schema
class UserBase(BaseModel):
    email: EmailStr = Field(..., description="User's email address.", example="user@example.com")

class Token(BaseModel):
    access_token: str = Field(..., description="JWT access token.")
    token_type: str = Field(default="bearer", description="Type of the token (e.g., 'bearer').")

class TokenPayload(BaseModel):
    sub: Optional[str] = Field(default=None, description="Subject of the token (User ID).", example="1")
    role: Optional[str] = Field(default=None, description="User role embedded in the token.", example="admin")

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="User's password (must be at least 8 characters).")
    role: UserRole = Field(default=UserRole.USER, description="Role to assign to the user.")
    is_active: bool = Field(default=True, description="Set to true if the user account should be active.")

    @validator("role", pre=True)
    def normalize_role(cls, v):
        """Convert role to lowercase for case-insensitive input."""
        if isinstance(v, str):
            return v.lower()
        return v

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(default=None, description="New email address for the user.", example="updateduser@example.com")
    password: Optional[str] = Field(default=None, min_length=8, description="New password (if changing, must be at least 8 characters).")
    role: Optional[UserRole] = Field(default=None, description="New role for the user.")
    is_active: Optional[bool] = Field(default=None, description="Update the active status of the user account.")

    @validator("role", pre=True)
    def normalize_role(cls, v):
        """Convert role to lowercase for case-insensitive input."""
        if isinstance(v, str):
            return v.lower()
        return v

class UserResponse(BaseModel):
    id: int = Field(..., description="Unique ID of the user.", example=1)
    email: EmailStr = Field(..., description="Email address of the user.", example="user@example.com")
    role: UserRole = Field(..., description="Role of the user.")
    is_active: bool = Field(..., description="Indicates if the user account is currently active.")
    created_at: datetime = Field(..., description="Timestamp when the user account was created (UTC).")
    updated_at: datetime = Field(..., description="Timestamp when the user account was last updated (UTC).")

    class Config:
        from_attributes = True

# UserListResponse schema
class UserListResponse(BaseModel):
    items: List[UserResponse] = Field(..., description="A list of user objects for the current page.")
    total: int = Field(..., description="Total number of users matching the query.", example=42)
    page: int = Field(..., description="The current page number (1-indexed).", example=1)
    size: int = Field(..., description="The number of items returned in this page.", example=10)
    pages: int = Field(..., description="Total number of pages available.", example=5)