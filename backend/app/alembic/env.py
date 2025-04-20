# backend/alembic/env.py (Standard Synchronous Version - Claude Suggestion)
from logging.config import fileConfig
import os
import sys

from sqlalchemy import engine_from_config # Use sync engine_from_config
from sqlalchemy import pool

from alembic import context

# --- Add project root to sys.path ---
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))
# --- End Path Addition ---

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)
from core.config import logger # Use logger from core config

# --- Import Base and models ---
try:
    from core.database import Base
    from models.user import User # Ensure models are imported
    target_metadata = Base.metadata
    logger.info("--- Successfully imported Base and User model in env.py ---")
except ImportError as e:
    logger.error(f"ERROR: Could not import Base or models in env.py: {e}")
    target_metadata = None

# Debug: Print the URL being read from alembic.ini
db_url_read = config.get_main_option('sqlalchemy.url')
logger.info(f"SQLAlchemy URL read from alembic.ini: {db_url_read[:db_url_read.find('@')] if db_url_read and '@' in db_url_read else db_url_read}") # Log safely

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    if not url: logger.error("sqlalchemy.url not configured"); return
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction(): context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode (Standard Synchronous version)."""
    try:
        connectable = engine_from_config(
            config.get_section(config.config_ini_section, {}),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )
    except Exception as e:
         logger.error(f"Error creating engine with engine_from_config: {e}", exc_info=True)
         raise

    with connectable.connect() as connection:
        logger.info("Successfully connected using engine_from_config.")
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            logger.info("Beginning transaction and running migrations...")
            context.run_migrations()
        logger.info("Migrations run complete (within online context).")

if context.is_offline_mode(): run_migrations_offline()
else: run_migrations_online()