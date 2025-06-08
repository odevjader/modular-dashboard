# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings, logger
# from app.core.module_loader import load_modules_config, discover_module_routers # Old imports removed
from app.core.module_loader import load_and_register_modules # New import
from app.api_router import api_router

# --- FastAPI App Initialization ---
openapi_url = f"{settings.API_PREFIX}/openapi.json" if settings.ENVIRONMENT == "development" else None
docs_url = "/docs" if settings.ENVIRONMENT == "development" else None
redoc_url = "/redoc" if settings.ENVIRONMENT == "development" else None

if not settings.PROJECT_NAME:
    logger.error("ERROR: Settings not loaded correctly in main.py, PROJECT_NAME is missing.")
    settings.PROJECT_NAME = "Fallback Project Name" # Ensure it has a value
if not settings.API_PREFIX:
    logger.error("ERROR: Settings not loaded correctly in main.py, API_PREFIX is missing.")
    settings.API_PREFIX = "/api" # Ensure it has a value


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=openapi_url,
    docs_url=docs_url,
    redoc_url=redoc_url,
    version="0.1.0"
)

# --- CORS Middleware Setup ---
allow_origins = []
if settings.BACKEND_CORS_ORIGINS:
    try:
        # Assuming BACKEND_CORS_ORIGINS is a list or comma-separated string in .env
        if isinstance(settings.BACKEND_CORS_ORIGINS, list):
            allow_origins = [str(origin).strip() for origin in settings.BACKEND_CORS_ORIGINS]
        elif isinstance(settings.BACKEND_CORS_ORIGINS, str):
             allow_origins = [origin.strip() for origin in settings.BACKEND_CORS_ORIGINS.split(",") if origin]
        else:
             logger.warning(f"BACKEND_CORS_ORIGINS has unexpected type: {type(settings.BACKEND_CORS_ORIGINS)}")
             allow_origins = []

    except Exception as e:
        logger.error(f"Error processing BACKEND_CORS_ORIGINS: {e}", exc_info=True)
        allow_origins = []

if allow_origins:
    logger.info(f"Configuring CORS for origins: {allow_origins}")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins,
          allow_credentials=True,
          allow_methods=["*"],
          allow_headers=["*"],
      )
else:
    logger.warning("No valid CORS origins found or specified (BACKEND_CORS_ORIGINS). CORS middleware not added.")

# --- Dynamically Load and Register Module Routers ---
try:
    logger.info("main.py: Starting dynamic module loading and registration process...")
    load_and_register_modules(api_router)
    logger.info("main.py: Dynamic module loading and registration process completed.")
except Exception as e:
    logger.critical(f"main.py: CRITICAL - Failed to load and register modules: {e}", exc_info=True)
    # Depending on the application's requirements, you might want to re-raise the exception
    # or exit the application if module loading is absolutely critical for startup.
    # For now, we log critically and allow the app to continue starting,
    # which might mean it runs with no (or only some) module routes.

# --- Include the Central API Router ---
# api_router should now have all dynamically loaded routes included by load_and_register_modules
try:
    logger.info(f"Including main API router with prefix: {settings.API_PREFIX}")
    app.include_router(api_router, prefix=settings.API_PREFIX)
    logger.info(f"Successfully included main API router. Check logs for dynamically loaded module routes.")
except NameError: # Should not happen if api_router is imported
    logger.error("api_router not defined before inclusion. Check imports in main.py.")
except Exception as e:
    logger.error(f"Error including main api_router: {e}", exc_info=True)


# --- Root Endpoint ---
@app.get("/", tags=["Root"])
async def read_root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME} - Now with Dynamic Modules!",
        "environment": settings.ENVIRONMENT,
        "docs_url": app.docs_url,
        "api_base_prefix": settings.API_PREFIX
        # "loaded_module_count" has been removed as discovered_routers_info is no longer in this scope.
        # Module loading status can be checked via logs from load_and_register_modules.
    }

logger.info(f"FastAPI application '{settings.PROJECT_NAME}' initialization complete.")