# backend/app/core/database.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base, DeclarativeBase
from typing import AsyncGenerator
from contextlib import asynccontextmanager
import logging  # Adicionado para criar instâncias de logger locais

# Apenas 'settings' é importado no topo.
from .config import settings

# Use the ASYNC Database URL from settings for the application engine
ASYNC_DATABASE_URL = settings.ASYNC_DATABASE_URL

async_engine = None
async_session_local = None

# Configure the async engine and session maker using the ASYNC URL
if not ASYNC_DATABASE_URL:
    print("ERROR: ASYNC_DATABASE_URL not set. Async database connection cannot be established.")
else:
    try:
        async_engine = create_async_engine(
            ASYNC_DATABASE_URL,
            echo=False,
        )
        async_session_local = async_sessionmaker(
            bind=async_engine,
            class_=AsyncSession,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False
        )
        print("INFO: SQLAlchemy async engine and session maker configured successfully.")
    except Exception as e:
        print(f"ERROR: Failed to configure SQLAlchemy async engine/session maker: {e}")
        async_engine = None
        async_session_local = None

# Base class for declarative class definitions
Base: DeclarativeBase = declarative_base()

# Dependency function for FastAPI endpoints to get a DB session
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that provides an SQLAlchemy AsyncSession.
    """
    logger = logging.getLogger(__name__)  # Cria instância de logger local
    if async_session_local is None:
        logger.error("Database session factory (async_session_local) is not configured.")
        raise RuntimeError("Database session factory is not available.")

    async with async_session_local() as session:
        logger.debug(f"Yielding database session: {session}")
        try:
            yield session
        except Exception:
            logger.exception("Exception during database session scope, rolling back.")
            await session.rollback()
            raise

@asynccontextmanager
async def get_db_contextmanager() -> AsyncGenerator[AsyncSession, None]:
    '''
    Provides an SQLAlchemy AsyncSession within an async context manager for scripts.
    '''
    logger = logging.getLogger(__name__)  # Cria instância de logger local
    if async_session_local is None:
        logger.error("Database session factory (async_session_local) is not configured.")
        raise RuntimeError("Database session factory is not available for context manager.")

    session: AsyncSession = async_session_local()
    logger.debug(f"Yielding database session from context manager: {session}")
    try:
        yield session
    except Exception:
        logger.exception("Exception within database context manager scope, rolling back.")
        await session.rollback()
        raise
    finally:
        logger.debug(f"Closing database session from context manager: {session}")
        await session.close()
