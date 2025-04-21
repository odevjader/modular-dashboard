from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from jose import jwt, JWTError
from pydantic import ValidationError
from typing import Annotated

from app.core import security
from app.core.database import get_db
from app.models import user as user_model
from app.modules.auth.v1 import schemas as auth_schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/v1/login")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> user_model.User:
    """
    Dependency to get the current user from the JWT token (Async).
    """
    try:
        payload = security.decode_token(token)
        if payload is None:
            raise credentials_exception

        subject = payload.get("sub")
        if subject is None:
            raise credentials_exception

        user_id = int(subject)

    except (JWTError, ValidationError, ValueError):
        raise credentials_exception

    result = await db.execute(
        select(user_model.User).where(user_model.User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[user_model.User, Depends(get_current_user)]
) -> user_model.User:
    """
    Dependency that gets the current user and checks if they are active.
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def require_admin_user(
    current_user: Annotated[user_model.User, Depends(get_current_active_user)]
) -> user_model.User:
    """
    Dependency that checks if the current user has admin role.
    """
    if current_user.role != user_model.UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user