# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings, logger
from app.core.module_loader import load_modules_config, discover_module_routers # New import
from app.api_router import api_router # api_router will be modified to use loaded routes

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

# --- Load Modules and Configure Routers ---
# This is the new section for dynamic module loading
try:
    logger.info("Initializing dynamic module loading sequence...")
    modules_configurations = load_modules_config() # Load from default path app/configs/modules.yaml

    # discovered_routers_info is a list of dicts:
    # [{"router": APIRouter_instance, "prefix": "/prefix", "tags": ["Tag"], "name": "module_name"}, ...]
    discovered_routers_info = discover_module_routers(modules_configurations)

    # The api_router (from app.api_router) will now be responsible for including these.
    # We need to make these discovered_routers_info available to api_router.py
    # One way: Pass it to a function in api_router.py
    # Another way: api_router.py imports and calls these functions itself (simpler for now)
    # For now, api_router.py will be modified to call these loader functions directly.
    # So, no explicit passing from main.py to api_router.py needed if api_router.py handles its own loading.
    logger.info("Dynamic module loading sequence initiated. Routers will be included via api_router.py.")

except FileNotFoundError:
    logger.error("CRITICAL: modules.yaml not found. No dynamic modules will be loaded. The application might not function as expected.")
except ValueError as ve:
    logger.error(f"CRITICAL: Error parsing modules.yaml or validating module configurations: {ve}. No dynamic modules will be loaded.")
except Exception as e:
    logger.error(f"CRITICAL: An unexpected error occurred during module loading: {e}", exc_info=True)
    # Depending on desired behavior, you might want to prevent app startup or run with core modules only.
    # For now, it will continue, and api_router will try to load what it can.


# --- Include the Central API Router ---
# api_router should now internally handle the inclusion of dynamically loaded routers
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
        "api_base_prefix": settings.API_PREFIX,
        "loaded_module_count": len(discovered_routers_info) if 'discovered_routers_info' in locals() else 0
    }

logger.info(f"FastAPI application '{settings.PROJECT_NAME}' initialization complete.")