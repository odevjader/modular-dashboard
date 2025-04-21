# backend/app/models/user.py
from sqlalchemy import Integer, String, Boolean, DateTime, func, Column
from sqlalchemy import Enum as SQLAlchemyEnum # <--- ADICIONADO Import Enum
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from datetime import datetime

# Import Base from database core setup
# Ajuste este import se sua Base estiver em outro lugar
from app.core.database import Base
# Importe o Enum recém-definido
from .enums import UserRole # <--- ADICIONADO Import UserRole

class User(Base):
    """
    SQLAlchemy model for the 'users' table.
    """
    __tablename__ = "users"

    # Primary Key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # User Credentials & Info
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    google_id: Mapped[Optional[str]] = mapped_column(String(255), unique=True, index=True, nullable=True)

    # Authorization & Status
    # --- LINHA ROLE MODIFICADA ---
    role: Mapped[UserRole] = mapped_column(
        SQLAlchemyEnum(UserRole, name="user_role_enum", create_type=True),
        default=UserRole.USER,
        nullable=False,
        index=True
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    def __repr__(self):
        # --- CORRIGIDO Typo: self.role (minúsculo) ---
        return f"<User(id={self.id}, email='{self.email}', role='{self.role.value}')>"