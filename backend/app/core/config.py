# backend/app/core/config.py
import logging
from pydantic_settings import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:5173", "[http://127.0.0.1:5173](http://127.0.0.1:5173)"]
    API_PREFIX: str = "/api"
    PROJECT_NAME: str = "Modular Dashboard API"
    LOGGING_LEVEL: int = logging.INFO # Default level

    # Google API Key
    GOOGLE_API_KEY: Optional[str] = None

    # Gemini Model Name - ADDED
    # Defaulting to a generally available model like 1.5 Flash
    GEMINI_MODEL_NAME: str = "gemini-2.0-flash-exp"

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()

# Configure logging level based on settings
logging.basicConfig(level=settings.LOGGING_LEVEL)
logger = logging.getLogger(__name__)

# Optional: Log loaded settings for verification
# logger.debug(f"Settings loaded: {settings.model_dump()}")
if not settings.GOOGLE_API_KEY:
    logger.warning("GOOGLE_API_KEY not found in environment/'.env' file.")
# logger.info(f"Using Gemini Model: {settings.GEMINI_MODEL_NAME}")