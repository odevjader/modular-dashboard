# backend/app/core/config.py
import logging
from pydantic_settings import BaseSettings
# Removed AnyHttpUrl import for simplicity here
from typing import List # Removed Union

class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    # Changed type hint to List[str] for simpler parsing from .env comma-separated list
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://127.0.0.1:5173"] # Example defaults
    API_PREFIX: str = "/api"
    PROJECT_NAME: str = "Modular Dashboard API"
    LOGGING_LEVEL: int = logging.INFO

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        # Pydantic v2 BaseSettings should handle comma-separated strings for List[str] automatically.

settings = Settings()

# Basic logging setup
logging.basicConfig(level=settings.LOGGING_LEVEL)
logger = logging.getLogger(__name__)
# logger.info(f"Logging configured via config.py. Level: {logging.getLevelName(settings.LOGGING_LEVEL)}")
# logger.info(f"Running {settings.PROJECT_NAME} in environment: {settings.ENVIRONMENT}")