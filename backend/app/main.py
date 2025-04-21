# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# --- IMPORTS CORRIGIDOS ---
# Import using absolute path from 'app' package root
from app.api_router import api_router
from app.core.config import settings, logger
# --- FIM IMPORTS CORRIGIDOS ---

# --- FastAPI App Initialization ---
openapi_url = f"{settings.API_PREFIX}/openapi.json" if settings.ENVIRONMENT == "development" else None
docs_url = "/docs" if settings.ENVIRONMENT == "development" else None
redoc_url = "/redoc" if settings.ENVIRONMENT == "development" else None

# Ensure settings object was loaded correctly
if not settings.PROJECT_NAME:
     # Fallback or error if settings didn't load
     print("ERROR: Settings not loaded correctly in main.py")
     settings.PROJECT_NAME = "Fallback Project Name"
     settings.API_PREFIX = "/api" # Provide fallback prefix

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


# --- Include the Central API Router ---
# Ensure api_router is correctly imported before using it
try:
    logger.info(f"Including main API router with prefix: {settings.API_PREFIX}")
    app.include_router(api_router, prefix=settings.API_PREFIX)
except NameError:
    logger.error("api_router not defined before inclusion. Check imports.")
except Exception as e:
    logger.error(f"Error including api_router: {e}", exc_info=True)


# --- Root Endpoint ---
@app.get("/", tags=["Root"])
async def read_root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "environment": settings.ENVIRONMENT,
        "docs_url": app.docs_url, # Use attribute from app instance
        "api_base_prefix": settings.API_PREFIX
    }

logger.info(f"FastAPI application '{settings.PROJECT_NAME}' initialization complete.")