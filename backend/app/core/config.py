# backend/app/core/config.py
import logging
from pydantic_settings import BaseSettings
from typing import List, Optional
from urllib.parse import urlparse
from functools import lru_cache
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:5173"]
    API_PREFIX: str = "/api"
    PROJECT_NAME: str = "Modular Dashboard API"
    LOGGING_LEVEL: int = logging.INFO

    # Google API Key
    GOOGLE_API_KEY: Optional[str] = None

    # Gemini Model Name
    GEMINI_MODEL_NAME: str = "gemini-2.0-flash-exp"

    # Database URLs
    DATABASE_URL: Optional[str] = None
    ASYNC_DATABASE_URL: Optional[str] = None

    # Database Credentials
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    # JWT Settings
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # Application Port
    APP_PORT: int = 8000

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        extra = "ignore"

# A função é mantida para carregar as configurações uma única vez.
# A lógica de logging foi removida para quebrar o ciclo de importação.
@lru_cache()
def get_settings() -> Settings:
    return Settings()

# A instância de settings é criada aqui para ser usada por toda a aplicação.
settings = get_settings()
