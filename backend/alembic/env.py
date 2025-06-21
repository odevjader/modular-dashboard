#backend/alembic/env.py
import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# Adiciona o diretório /app ao sys.path para que os módulos sejam encontrados
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- CORREÇÃO: Importa Base e modelos usando o caminho absoluto do pacote 'app' ---
try:
    from app.core.database import Base
    from app.models.user import User
    from app.models.enums import UserRole
    from app.models.document import Document, DocumentChunk # Ensure new models are imported

    target_metadata = Base.metadata
    print("Successfully imported models and set target_metadata")
except ImportError as e:
    print(f"ERROR: Could not import models: {e}")
    Base = None # Ensure Base is None if import fails
    target_metadata = None

# ---- O resto do arquivo ----

# ---- This block was for debugging and is now removed ----
def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()