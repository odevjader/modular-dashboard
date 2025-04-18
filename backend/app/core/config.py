# backend/app/core/config.py
import logging
from pydantic_settings import BaseSettings
from typing import List, Optional # Import Optional

class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]
    API_PREFIX: str = "/api"
    PROJECT_NAME: str = "Modular Dashboard API"
    LOGGING_LEVEL: int = logging.INFO

    # Google API Key - Marked as Optional[str] so app can start if not set,
    # but endpoints using it should check if it exists. Default is None.
    GOOGLE_API_KEY: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()

# Basic logging setup
logging.basicConfig(level=settings.LOGGING_LEVEL)
logger = logging.getLogger(__name__)
# logger.info(f"Logging configured via config.py. Level: {logging.getLevelName(settings.LOGGING_LEVEL)}")
# logger.info(f"Running {settings.PROJECT_NAME} in environment: {settings.ENVIRONMENT}")

# Check if the key was loaded (optional logging for debug)
# if settings.GOOGLE_API_KEY:
#     logger.debug("GOOGLE_API_KEY loaded.")
# else:
#     logger.warning("GOOGLE_API_KEY not found in environment/'.env' file.")