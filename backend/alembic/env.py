#backend/alembic/env.py
import os
import sys
from logging.config import fileConfig

from sqlalchemy import create_engine, pool
from alembic import context

# Adiciona o diretório /app ao sys.path para que os módulos sejam encontrados
# Isso assume que o diretório 'backend' é o diretório pai de 'alembic' e 'app'
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'app')))
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))


config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- Import models and settings ---
try:
    from app.core.database import Base
    # Import all models here so Alembic can detect changes
    from app.models import User, UserRole, Document, DocumentChunk
    from app.core.config import settings # Import settings

    target_metadata = Base.metadata
    print("Successfully imported models and settings, target_metadata is set.")
except ImportError as e:
    print(f"ERROR: Could not import models or settings: {e}")
    target_metadata = None
    # Exit if critical components cannot be imported
    sys.exit(f"Alembic configuration failed due to import error: {e}")


# Use DATABASE_URL from settings for migrations
# Ensure DATABASE_URL uses a synchronous dialect (e.g., postgresql+psycopg2)
# Alembic typically uses the synchronous URL.
db_url = settings.DATABASE_URL
if not db_url:
    print("ERROR: DATABASE_URL not found in settings. Please check your .env file and config.")
    sys.exit("DATABASE_URL is required for Alembic migrations.")
# Replace asyncpg with psycopg2 if ASYNC_DATABASE_URL was mistakenly used or adapt
# This ensures Alembic uses a sync driver if DATABASE_URL was set to an async one.
if db_url.startswith("postgresql+asyncpg"):
    db_url = db_url.replace("postgresql+asyncpg", "postgresql+psycopg2", 1)
elif db_url.startswith("postgresql://"): # common for psycopg2 or if no driver specified
    # Assuming psycopg2 is intended if no specific +driver is present
    # No change needed if it's already `postgresql://` and psycopg2 is default or installed
    pass


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.
    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.
    Calls to context.execute() here emit the given string to the
    script output.
    """
    context.configure(
        url=db_url, # Use db_url from settings
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode.
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    # Create engine programmatically using db_url from settings
    connectable = create_engine(db_url, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

if target_metadata is None:
    print("ERROR: target_metadata is None. Migrations cannot run without model metadata.")
    sys.exit("Failed to initialize Alembic context due to missing target_metadata.")

if context.is_offline_mode():
    print(f"Running migrations offline with URL: {db_url[:db_url.find('@') if '@' in db_url else len(db_url)]}...") # Log URL without credentials
    run_migrations_offline()
else:
    print(f"Running migrations online with URL: {db_url[:db_url.find('@') if '@' in db_url else len(db_url)]}...") # Log URL without credentials
    run_migrations_online()
