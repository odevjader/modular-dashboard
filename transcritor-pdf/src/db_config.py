import asyncpg
import os
import logging

logger = logging.getLogger(__name__)

# Attempt to use ASYNC_DATABASE_URL first, then DATABASE_URL
# The default value is a placeholder and should ideally not be used if .env is set up correctly.
ASYNC_DB_URL_FROM_ENV = os.getenv("ASYNC_DATABASE_URL")
DB_URL_FROM_ENV = os.getenv("DATABASE_URL")

if ASYNC_DB_URL_FROM_ENV:
    DATABASE_URL = ASYNC_DB_URL_FROM_ENV
    logger.info(f"Using ASYNC_DATABASE_URL for transcritor-pdf: {DATABASE_URL}")
elif DB_URL_FROM_ENV:
    # If using a sync URL for an async app, ensure it's adapted if necessary,
    # though asyncpg typically expects the connection string without a specific +driver.
    # For simplicity, we'll assume it's compatible or will be made so.
    DATABASE_URL = DB_URL_FROM_ENV
    logger.info(f"Using DATABASE_URL for transcritor-pdf: {DATABASE_URL}")
    # Potentially adapt if it's a sync-only DSN like 'postgresql://...' for asyncpg
    if not DATABASE_URL.startswith("postgresql+asyncpg://") and DATABASE_URL.startswith("postgresql://"):
         # This basic replacement might not cover all cases but is a common adaptation.
         # DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
         # logger.info(f"Adapted DATABASE_URL for asyncpg: {DATABASE_URL}")
         # For now, let's assume the URL provided in .env is suitable or will be adjusted there.
         pass # Keep it simple, rely on .env to provide a compatible URL
else:
    # Fallback if neither is set (should not happen in a configured environment)
    DATABASE_URL = "postgresql+asyncpg://user:pass@host:port/db" # Placeholder
    logger.warning("Neither ASYNC_DATABASE_URL nor DATABASE_URL found in environment. Using placeholder for transcritor-pdf.")

# The rest of the file (db_pool, connect_to_db, close_db_connection)
# will use this DATABASE_URL.

# Placeholder for embedding dimensions - this might come from a model config later
# For now, common dimensions are 384 (e.g., all-MiniLM-L6-v2), 768 (e.g., BERT base), 1536 (OpenAI Ada-002)
EMBEDDING_DIMENSIONS = int(os.getenv("EMBEDDING_DIMENSIONS", "1536"))

# Global variable for the connection pool
# Explicitly type hint that it can be None initially
db_pool: asyncpg.Pool | None = None

async def connect_to_db():
    """
    Establishes a connection pool to the PostgreSQL database.
    The pool is stored in the global `db_pool` variable.
    """
    global db_pool
    if db_pool is not None:
        logger.info("Database connection pool already exists.")
        return

    logger.info(f"Attempting to connect to database using URL: {DATABASE_URL}") # Updated log message
    try:
        pool = await asyncpg.create_pool(
            dsn=DATABASE_URL,
            min_size=int(os.getenv("DB_POOL_MIN_SIZE", "1")),
            max_size=int(os.getenv("DB_POOL_MAX_SIZE", "10")),
            # Add other pool settings if needed, e.g., timeouts
            # command_timeout=60,  # Example: Default command timeout for connections from this pool
        )
        if pool:
            db_pool = pool
            logger.info("Successfully connected to the database and created connection pool.")
            # Optionally, test the connection with a simple query
            async with db_pool.acquire() as conn:
                await conn.fetchval("SELECT 1")
            logger.info("Database connection pool test query successful.")
        else:
            logger.error("asyncpg.create_pool returned None. Pool creation failed.")
            # This case should ideally not happen if create_pool doesn't raise an exception
            # but it's good to be aware of.

    except asyncpg.exceptions.PostgresError as pe: # More specific asyncpg errors
        logger.error(f"PostgreSQL error while connecting to the database: {pe}")
        # Depending on the app's needs, you might want to sys.exit() or raise
    except Exception as e:
        logger.error(f"Failed to connect to the database and create pool: {e}", exc_info=True)
        # Optionally re-raise or handle as appropriate for startup (e.g., sys.exit for critical failure)
        # raise # Re-raise if you want the application to fail on startup if DB connection fails

async def close_db_connection():
    """
    Closes the database connection pool if it exists.
    """
    global db_pool
    if db_pool:
        logger.info("Closing database connection pool...")
        try:
            await db_pool.close()
            db_pool = None # Ensure it's reset
            logger.info("Database connection pool closed successfully.")
        except Exception as e:
            logger.error(f"Error while closing database connection pool: {e}", exc_info=True)
    else:
        logger.info("No active database connection pool to close.")

# Example of how to use (typically called at app startup/shutdown):
# async def main_app_lifecycle():
#     await connect_to_db()
#     # ... your application runs ...
#     if db_pool: # Check if pool was successfully created
#         # Example usage
#         async with db_pool.acquire() as conn:
#             val = await conn.fetchval("SELECT $1::TEXT", "Hello DB")
#             print(f"Test query result: {val}")
#     await close_db_connection()

# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO) # Ensure logger is configured for standalone run
#     asyncio.run(main_app_lifecycle())
