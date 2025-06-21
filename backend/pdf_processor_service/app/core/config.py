from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    SERVICE_NAME: str = "PDF Processor Service"
    LOGGING_LEVEL: int = 20 # INFO

    # Database Configuration (sync URL for SQLAlchemy, as this service might not use async for DB ops directly)
    # If async is needed later, an ASYNC_DATABASE_URL can be added.
    DATABASE_URL: str = "postgresql://user:password@db:5432/appdb" # Default, will be overridden by .env

    # Placeholder for other service-specific settings
    # EXAMPLE_SETTING: str = "default_value"

settings = Settings()
