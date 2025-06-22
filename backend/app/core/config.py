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
    GEMINI_MODEL_NAME: str = "gemini-2.0-flash-exp"

    # Database URLs
    DATABASE_URL: Optional[str] = None # Sync URL (primarily for Alembic reflection)
    ASYNC_DATABASE_URL: Optional[str] = None # Async URL (for application) - ADDED

    # Database Credentials (used by Alembic and potentially app)
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    # JWT Settings
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # Application Port
    APP_PORT: int = 8000

    # Microservice URLs
    PDF_PROCESSOR_SERVICE_URL: str = "http://pdf_processor_service:8000"

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        # Allow extra fields from environment variables
        extra = "allow" # Or "ignore" if we don't want to define all env vars

# settings = Settings() # Defer instantiation

# Function to get settings, allowing for deferred initialization
_settings_instance = None

def get_settings() -> Settings:
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = Settings()

        # Configure logging once settings are loaded
        logging.basicConfig(level=_settings_instance.LOGGING_LEVEL)
        logger = logging.getLogger(__name__) # Re-get logger after basicConfig

        # Log warnings for missing critical settings
        if not _settings_instance.GOOGLE_API_KEY: logger.warning("GOOGLE_API_KEY not found.")
        if not _settings_instance.DATABASE_URL: logger.warning("DATABASE_URL (sync) not found.")
        if not _settings_instance.ASYNC_DATABASE_URL:
            logger.warning("ASYNC_DATABASE_URL not found. App DB operations will fail.")
        else:
            try:
                parsed_url = urlparse(_settings_instance.ASYNC_DATABASE_URL)
                safe_url = f"{parsed_url.scheme}://{parsed_url.username}@{parsed_url.hostname}:{parsed_url.port}{parsed_url.path}"
                logger.info(f"Async Database URL loaded: {safe_url}")
            except Exception:
                logger.info("Async Database URL loaded (details hidden).")
    return _settings_instance

settings = get_settings() # Initial call to load for normal operation

# Configure logging - Moved into get_settings to ensure it runs after settings are loaded
# logging.basicConfig(level=settings.LOGGING_LEVEL) # This would use potentially uninitialized settings
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