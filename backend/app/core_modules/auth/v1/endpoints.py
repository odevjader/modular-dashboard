# backend/app/core_modules/auth/v1/endpoints.py
from fastapi import APIRouter, Depends, HTTPException, status, Query # Added Query
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

@router.get("/users/me", response_model=auth_schemas.UserResponse) # Changed UserRead to UserResponse
def read_users_me(
    current_user: Annotated[user_model.User, Depends(get_current_active_user)]
):
    """Get current logged-in user's information."""
    return current_user

# Removed: from app.core.security import hash_password (use security.hash_password directly)

@router.post("/admin/users", response_model=auth_schemas.UserResponse) # Changed UserRead to UserResponse
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

    hashed_password = security.hash_password(user_in.password) # Use security.hash_password
    db_user = user_model.User(
        email=user_in.email, # email is inherited via UserBase in UserCreate
        hashed_password=hashed_password,
        role=user_in.role,
        is_active=user_in.is_active # Set is_active from user_in
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

@router.get("/admin/users", response_model=auth_schemas.UserListResponse) # Changed to UserListResponse
async def list_users(
    db: AsyncSession = Depends(get_db),
    admin_user: user_model.User = Depends(require_admin_user),
    skip: int = Query(0, ge=0, description="Number of items to skip"), # Added skip
    limit: int = Query(10, ge=1, le=100, description="Number of items to return per page") # Added limit
):
    """List all users (admin only) with pagination."""
    total_count_stmt = select(func.count(user_model.User.id))
    total_count_result = await db.execute(total_count_stmt)
    total_count = total_count_result.scalar_one()

    users_stmt = select(user_model.User).order_by(user_model.User.id).offset(skip).limit(limit) # Added order_by for consistency
    users_result = await db.execute(users_stmt)
    users = users_result.scalars().all()

    current_page = (skip // limit) + 1 if limit > 0 else 1
    total_pages = (total_count + limit - 1) // limit if limit > 0 else 0

    return auth_schemas.UserListResponse(
        items=users,
        total=total_count,
        page=current_page,
        size=len(users), # Actual number of items returned in this page
        pages=total_pages
    )

@router.get("/admin/users/{user_id}", response_model=auth_schemas.UserResponse)
async def get_user_by_id(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    admin_user: user_model.User = Depends(require_admin_user)
):
    """Get a specific user by their ID (admin only)."""
    stmt = select(user_model.User).where(user_model.User.id == user_id)
    result = await db.execute(stmt)
    db_user = result.scalars().first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user

@router.put("/admin/users/{user_id}", response_model=auth_schemas.UserResponse) # Changed UserRead to UserResponse
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Update logic using model attribute assignment
    update_data = user_in.dict(exclude_unset=True)

    if 'email' in update_data and update_data['email'] != db_user.email:
        # Check if the new email is already taken by another user
        email_check_stmt = select(user_model.User).where(user_model.User.email == update_data['email'])
        if await db.execute(email_check_stmt).scalar_one_or_none():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered by another user")
        db_user.email = update_data['email']

    if 'password' in update_data and update_data['password'] is not None:
        db_user.hashed_password = security.hash_password(update_data['password'])
    
    if 'role' in update_data and update_data['role'] is not None:
        db_user.role = update_data['role']

    if 'is_active' in update_data and update_data['is_active'] is not None:
        db_user.is_active = update_data['is_active']

    db.add(db_user) # Add the modified instance to the session
    await db.commit()
    await db.refresh(db_user) # Refresh to get any DB-side changes
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