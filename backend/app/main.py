# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Use get_settings() for deferred initialization
from app.core.config import get_settings, logger
from app.core.module_loader import load_and_register_modules
from app.api_router import api_router

# Initialize settings by calling get_settings()
# This ensures that if this is the first time settings are accessed (e.g. by tests after patching env vars),
# they are loaded with the correct (potentially mocked) environment.
settings = get_settings()

# --- FastAPI App Initialization ---
# Now use the 'settings' instance obtained from get_settings()
openapi_url = f"{settings.API_PREFIX}/openapi.json" if settings.ENVIRONMENT == "development" else None
docs_url = "/docs" if settings.ENVIRONMENT == "development" else None
redoc_url = "/redoc" if settings.ENVIRONMENT == "development" else None

if not settings.PROJECT_NAME:
    logger.error("ERROR: Settings not loaded correctly in main.py, PROJECT_NAME is missing.")
    # This fallback might be less necessary if get_settings() ensures proper loading
    settings.PROJECT_NAME = "Fallback Project Name"
if not settings.API_PREFIX:
    logger.error("ERROR: Settings not loaded correctly in main.py, API_PREFIX is missing.")
    settings.API_PREFIX = "/api"


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
        if isinstance(settings.BACKEND_CORS_ORIGINS, list):
            allow_origins = [str(origin).strip() for origin in settings.BACKEND_CORS_ORIGINS]
        elif isinstance(settings.BACKEND_CORS_ORIGINS, str):
             allow_origins = [origin.strip() for origin in settings.BACKEND_CORS_ORIGINS.split(",") if origin]
        else:
             logger.warning(f"BACKEND_CORS_ORIGINS has unexpected type: {type(settings.BACKEND_CORS_ORIGINS)}")
             allow_origins = [] # Default to empty if type is unexpected
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
    load_and_register_modules(api_router) # api_router is imported from app.api_router
    logger.info("main.py: Dynamic module loading and registration process completed.")
except Exception as e:
    logger.critical(f"main.py: CRITICAL - Failed to load and register modules: {e}", exc_info=True)

# --- Include the Central API Router ---
try:
    logger.info(f"Including main API router with prefix: {settings.API_PREFIX}")
    app.include_router(api_router, prefix=settings.API_PREFIX)
    logger.info(f"Successfully included main API router. Check logs for dynamically loaded module routes.")
except Exception as e: # Catch a more general exception if api_router itself is problematic
    logger.error(f"Error including main api_router: {e}", exc_info=True)


# --- Root Endpoint ---
@app.get("/", tags=["Root"])
async def read_root():
    # Access settings through the get_settings() function if you want to be absolutely sure
    # about getting the most up-to-date instance, though the global 'settings' should be fine here.
    current_settings = get_settings()
    return {
        "message": f"Welcome to {current_settings.PROJECT_NAME} - Now with Dynamic Modules!",
        "environment": current_settings.ENVIRONMENT,
        "docs_url": app.docs_url, # app.docs_url is fine as it's set on app init
        "api_base_prefix": current_settings.API_PREFIX
    }

logger.info(f"FastAPI application '{settings.PROJECT_NAME}' initialization complete.")