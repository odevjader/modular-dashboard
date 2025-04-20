# backend/app/core/database.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base, DeclarativeBase
from core.config import settings, logger # Import settings and logger
from typing import AsyncGenerator

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
        # Raising error might be better than yielding None if DB is critical
        raise RuntimeError("Database session factory is not available.")
        # yield None # Yielding None will likely cause AttributeError in endpoint

    # Create a session for the request
    async with async_session_local() as session:
        logger.debug(f"Yielding database session: {session}")
        try:
            yield session
        except Exception:
            # Rollback in case of exception during request handling
            logger.exception("Exception during database session scope, rolling back.")
            await session.rollback()
            raise
        # Session is automatically closed by 'async with'