# backend/app/core_modules/auth/v1/endpoints.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func
from typing import Annotated, List
import logging

from . import schemas as auth_schemas
from app.models import user as user_model
from app.core import security
from app.core.database import get_db
from app.core.dependencies import get_current_active_user, require_admin_user

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/login", response_model=auth_schemas.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_db)
):
    """OAuth2 compatible token login."""
    username = form_data.username.strip()
    logger.info(f"Login attempt for email: '{username}', password: {form_data.password[:3]}..., raw username: {repr(form_data.username)}")
    stmt = select(user_model.User).where(func.lower(user_model.User.email) == func.lower(username))
    logger.info(f"Executing query: {str(stmt)}")
    result = await db.execute(stmt)
    user = result.scalars().first()
    
    if not user:
        logger.error(f"User not found: '{username}', query: {str(stmt)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    logger.info(f"User found: {user.email}, active: {user.is_active}, hash: {user.hashed_password[:10]}...")
    
    if not user.hashed_password:
        logger.error(f"No hashed password for {user.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not security.verify_password(form_data.password, user.hashed_password):
        logger.error(f"Password verification failed for {user.email}, input: {form_data.password[:3]}...")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        logger.error(f"User {user.email} is inactive")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )

    token_data = {
        "sub": str(user.id),
        "role": user.role.value
    }
    access_token = security.create_access_token(data=token_data)
    logger.info(f"Login successful for {user.email}, token issued")

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
        role=user_in.role,
        is_active=True
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

@router.get("/admin/users", response_model=List[auth_schemas.UserRead])
async def list_users(
    db: AsyncSession = Depends(get_db),
    admin_user: user_model.User = Depends(require_admin_user)
):
    """List all users (admin only)."""
    stmt = select(user_model.User)
    result = await db.execute(stmt)
    users = result.scalars().all()
    return users

@router.put("/admin/users/{user_id}", response_model=auth_schemas.UserRead)
async def update_user(
    user_id: int,
    user_in: auth_schemas.UserUpdate,
    db: AsyncSession = Depends(get_db),
    admin_user: user_model.User = Depends(require_admin_user)
):
    """Update a user (admin only)."""
    stmt = select(user_model.User).where(user_model.User.id == user_id)
    result = await db.execute(stmt)
    db_user = result.scalars().first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_in.email:
        email_check = select(user_model.User).where(user_model.User.email == user_in.email, user_model.User.id != user_id)
        if await db.execute(email_check).scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Email already registered")

    update_data = user_in.dict(exclude_unset=True)
    if 'password' in update_data:
        update_data['hashed_password'] = hash_password(update_data.pop('password'))
    
    await db.execute(
        update(user_model.User).where(user_model.User.id == user_id).values(**update_data)
    )
    await db.commit()
    await db.refresh(db_user)
    return db_user

@router.delete("/admin/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    admin_user: user_model.User = Depends(require_admin_user)
):
    """Delete a user (admin only)."""
    stmt = select(user_model.User).where(user_model.User.id == user_id)
    result = await db.execute(stmt)
    db_user = result.scalars().first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.execute(delete(user_model.User).where(user_model.User.id == user_id))
    await db.commit()