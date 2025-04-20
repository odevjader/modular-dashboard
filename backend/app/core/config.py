# backend/app/core/config.py
import logging
from pydantic_settings import BaseSettings
from typing import List, Optional
from urllib.parse import urlparse # For safe logging

class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:5173", "[http://127.0.0.1:5173](http://127.0.0.1:5173)"]
    API_PREFIX: str = "/api"
    PROJECT_NAME: str = "Modular Dashboard API"
    LOGGING_LEVEL: int = logging.INFO

    # Google API Key
    GOOGLE_API_KEY: Optional[str] = None

    # Gemini Model Name
    GEMINI_MODEL_NAME: str = "gemini-1.5-flash-latest"

    # Database URLs
    DATABASE_URL: Optional[str] = None # Sync URL (primarily for Alembic reflection)
    ASYNC_DATABASE_URL: Optional[str] = None # Async URL (for application) - ADDED

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()

# Configure logging
logging.basicConfig(level=settings.LOGGING_LEVEL)
logger = logging.getLogger(__name__)

# Log warnings for missing critical settings
if not settings.GOOGLE_API_KEY: logger.warning("GOOGLE_API_KEY not found.")
if not settings.DATABASE_URL: logger.warning("DATABASE_URL (sync) not found.") # Used by Alembic internals potentially
if not settings.ASYNC_DATABASE_URL: # ADDED Check
    logger.warning("ASYNC_DATABASE_URL not found. App DB operations will fail.")
else:
    # Log partial async URL for confirmation, hiding password
    try:
        parsed_url = urlparse(settings.ASYNC_DATABASE_URL)
        safe_url = f"{parsed_url.scheme}://{parsed_url.username}@{parsed_url.hostname}:{parsed_url.port}{parsed_url.path}"
        logger.info(f"Async Database URL loaded: {safe_url}")
    except Exception:
         logger.info("Async Database URL loaded (details hidden).")

# logger.info(f"Using Gemini Model: {settings.GEMINI_MODEL_NAME}")