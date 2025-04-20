# backend/app/models/user.py
from sqlalchemy import Integer, String, Boolean, DateTime, func, Column
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from datetime import datetime

# Import Base from database core setup
from core.database import Base

class User(Base):
    """
    SQLAlchemy model for the 'users' table.
    """
    __tablename__ = "users"

    # Primary Key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # User Credentials & Info
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    # Storing hashed password, nullable if using only external auth initially
    hashed_password: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    # Store Google's unique ID for Google Sign-In
    google_id: Mapped[Optional[str]] = mapped_column(String(255), unique=True, index=True, nullable=True)

    # Authorization & Status
    role: Mapped[str] = mapped_column(String(50), default='user', nullable=False) # e.g., 'user', 'admin'
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', role='{self.role}')>"