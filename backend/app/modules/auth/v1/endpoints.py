from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Annotated

from . import schemas as auth_schemas
from app.models import user as user_model
from app.core import security
from app.core.database import get_db
from app.core.dependencies import get_current_active_user, require_admin_user

router = APIRouter()

@router.post("/login", response_model=auth_schemas.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_db)
):
    """OAuth2 compatible token login."""
    stmt = select(user_model.User).where(user_model.User.email == form_data.username)
    result = await db.execute(stmt)
    user = result.scalars().first()

    if not user or not user.hashed_password or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
         raise HTTPException(
             status_code=status.HTTP_400_BAD_REQUEST,
             detail="Inactive user"
         )

    token_data = {
        "sub": str(user.id),
        "role": user.role.value
    }
    access_token = security.create_access_token(data=token_data)

    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=auth_schemas.UserRead)
def read_users_me(
    current_user: Annotated[user_model.User, Depends(get_current_active_user)]
):
    """Get current logged-in user's information."""
    return current_user

from app.core.security import hash_password

@router.post("/admin/users", response_model=auth_schemas.UserRead)
async def create_user(
    user_in: auth_schemas.UserCreate,
    db: AsyncSession = Depends(get_db),
    admin_user: user_model.User = Depends(require_admin_user)
):
    """Create a new user (admin only)."""
    stmt = select(user_model.User).where(user_model.User.email == user_in.email)
    result = await db.execute(stmt)
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user_in.password)
    db_user = user_model.User(
        email=user_in.email,
        hashed_password=hashed_password,
        role=user_in.role,  # Use role from input
        is_active=True
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user