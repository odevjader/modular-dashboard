import os
from datetime import datetime, timedelta, timezone
from typing import Any, Union
from jose import jwt, JWTError
from passlib.context import CryptContext
import logging

logger = logging.getLogger(__name__)

# --- Password Hashing ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    logger.info(f"Verifying password for plain: {plain_password[:3]}..., hashed: {hashed_password[:10]}...")
    try:
        result = pwd_context.verify(plain_password, hashed_password)
        logger.info(f"Password verification result: {result}")
        return result
    except Exception as e:
        logger.error(f"Password verification failed: {str(e)}")
        return False

def hash_password(password: str) -> str:
    logger.info(f"Hashing password for: {password[:3]}...")
    hashed = pwd_context.hash(password)
    logger.info(f"Generated hash: {hashed[:10]}...")
    return hashed

# --- JWT Handling ---
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440")) # Using 24h default

if not SECRET_KEY:
    logger.error("CRITICAL ERROR: SECRET_KEY environment variable not set.")
    SECRET_KEY = "please_set_a_real_secret_key_in_env" # Insecure fallback

def create_access_token(
    data: dict, expires_delta: Union[timedelta, None] = None
) -> str:
    """
    Generates a JWT access token adding expiration to the provided data.

    :param data: Dictionary containing claims like 'sub', 'role'.
    :param expires_delta: Optional timedelta for expiration. Uses default if None.
    :return: Encoded JWT access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> dict | None:
    """
    Decodes a JWT token and returns its payload.

    :param token: JWT token string.
    :return: Decoded payload as dict, or None if invalid.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None