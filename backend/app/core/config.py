# backend/app/core/config.py
import logging
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl # Correct import for Pydantic v2
from typing import List, Union # Union might be needed depending on .env format

class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    # Ensure .env uses comma-separated strings or JSON list for URLs
    BACKEND_CORS_ORIGINS: List[Union[AnyHttpUrl, str]] = ["http://localhost:5173", "[http://127.0.0.1:5173](http://127.0.0.1:5173)"] # Example defaults
    API_PREFIX: str = "/api"
    PROJECT_NAME: str = "Modular Dashboard API"
    LOGGING_LEVEL: int = logging.INFO

    class Config:
        env_file = ".env" # Looks for .env in the same dir as this config file is run from, or needs full path
        # To ensure it finds backend/.env, Pydantic-settings looks up the directory tree,
        # or we might need to specify the path more explicitly if issues arise.
        # Let's assume default behavior works first.
        env_file_encoding = 'utf-8'

settings = Settings()

# Basic logging setup
logging.basicConfig(level=settings.LOGGING_LEVEL)
logger = logging.getLogger(__name__)
# logger.info(f"Logging configured via config.py. Level: {logging.getLevelName(settings.LOGGING_LEVEL)}")
# logger.info(f"Running {settings.PROJECT_NAME} in environment: {settings.ENVIRONMENT}")