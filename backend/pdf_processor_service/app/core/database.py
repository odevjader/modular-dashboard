from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings # Import settings from the same directory

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Create SQLAlchemy engine
# For simplicity, using a synchronous engine. If async operations are needed later,
# this can be changed to create_async_engine from sqlalchemy.ext.asyncio.
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a SessionLocal class, which will be a factory for new Session objects
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class for declarative class definitions
Base = declarative_base()

# Dependency function for FastAPI endpoints to get a DB session
def get_db():
    """
    FastAPI dependency that provides an SQLAlchemy Session.
    Ensures the session is closed afterwards.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
