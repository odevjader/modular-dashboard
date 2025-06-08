# backend/app/core/database.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base, DeclarativeBase
# --- IMPORT CORRIGIDO ---
from .config import settings, logger # Import settings and logger usando ponto (.)
# --- FIM IMPORT CORRIGIDO ---
from typing import AsyncGenerator
from contextlib import asynccontextmanager # Added import

# Use the ASYNC Database URL from settings for the application engine
ASYNC_DATABASE_URL = settings.ASYNC_DATABASE_URL

async_engine = None
async_session_local = None

# Configure the async engine and session maker using the ASYNC URL
if not ASYNC_DATABASE_URL:
    logger.error("ASYNC_DATABASE_URL not set. Async database connection cannot be established.")
else:
    try:
        # Create the SQLAlchemy async engine using the ASYNC URL
        async_engine = create_async_engine(
            ASYNC_DATABASE_URL, # Use the async URL here
            echo=False, # Set to True to see generated SQL in app logs
        )

        # Create an async session factory
        async_session_local = async_sessionmaker(
            bind=async_engine,
            class_=AsyncSession,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False
        )
        logger.info("SQLAlchemy async engine and session maker configured successfully using ASYNC_DATABASE_URL.")
    except Exception as e:
        logger.error(f"Failed to configure SQLAlchemy async engine/session maker using ASYNC_DATABASE_URL: {e}", exc_info=True)
        # Ensure these are None if setup fails
        async_engine = None
        async_session_local = None

# Base class for declarative class definitions
Base: DeclarativeBase = declarative_base()

# Dependency function for FastAPI endpoints to get a DB session
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that provides an SQLAlchemy AsyncSession.
    Ensures the session is closed afterwards.
    """
    if async_session_local is None:
        logger.error("Database session factory (async_session_local) is not configured. Cannot get DB session.")
        raise RuntimeError("Database session factory is not available.")

    # Create a session for the request
    async with async_session_local() as session:
        logger.debug(f"Yielding database session: {session}")
        try:
            yield session
        except Exception:
            logger.exception("Exception during database session scope, rolling back.")
            await session.rollback()
            raise
        # Session is automatically closed by 'async with'

@asynccontextmanager
async def get_db_contextmanager() -> AsyncGenerator[AsyncSession, None]:
    '''
    Provides an SQLAlchemy AsyncSession within an async context manager.
    Ensures the session is closed afterwards.
    Useful for scripts or background tasks.
    '''
    if async_session_local is None:
        logger.error("Database session factory (async_session_local) is not configured. Cannot get DB session.")
        # Or raise an exception, depending on desired behavior for scripts
        raise RuntimeError("Database session factory (async_session_local) is not available for context manager.")

    session: AsyncSession = async_session_local()
    logger.debug(f"Yielding database session from context manager: {session}")
    try:
        yield session
        # For scripts, we might want to commit if no exceptions occurred,
        # but typically the calling code should handle commits.
        # await session.commit() # Optional: if you want auto-commit on successful exit
    except Exception:
        logger.exception("Exception within database context manager scope, rolling back.")
        await session.rollback()
        raise
    finally:
        logger.debug(f"Closing database session from context manager: {session}")
        await session.close()