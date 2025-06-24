# backend/app/main.py
import logging
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# --- IMPORT CORRIGIDO ---
# Importa apenas get_settings de config.py. O logger será configurado aqui.
from app.core.config import get_settings
from app.core.module_loader import load_and_register_modules
from app.api_router import api_router
# --- FIM IMPORT CORRIGIDO ---


# Initialize settings by calling get_settings()
settings = get_settings()

# --- CONFIGURAÇÃO DE LOGGING ---
# A configuração do logger é feita aqui, no ponto de entrada da aplicação,
# após as configurações (settings) terem sido carregadas.
logging.basicConfig(level=settings.LOGGING_LEVEL, stream=sys.stdout, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
# --- FIM DA CONFIGURAÇÃO ---


# --- FastAPI App Initialization ---
openapi_url = f"{settings.API_PREFIX}/openapi.json" if settings.ENVIRONMENT == "development" else None
docs_url = "/docs" if settings.ENVIRONMENT == "development" else None
redoc_url = "/redoc" if settings.ENVIRONMENT == "development" else None

if not settings.PROJECT_NAME:
    logger.error("ERROR: Settings not loaded correctly in main.py, PROJECT_NAME is missing.")
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
    load_and_register_modules(api_router) # api_router is imported from app.api_router
    logger.info("main.py: Dynamic module loading and registration process completed.")
except Exception as e:
    logger.critical(f"main.py: CRITICAL - Failed to load and register modules: {e}", exc_info=True)

# --- Include the Central API Router ---
try:
    logger.info(f"Including main API router with prefix: {settings.API_PREFIX}")
    app.include_router(api_router, prefix=settings.API_PREFIX)
    logger.info(f"Successfully included main API router. Check logs for dynamically loaded module routes.")

    # --- Log all registered routes for debugging ---
    logger.info("--- BEGIN REGISTERED ROUTES ---")
    for route in app.routes:
        if hasattr(route, "path"):
            logger.info(f"Path: {route.path}, Name: {route.name}, Methods: {getattr(route, 'methods', None)}")
        # For mounted APIRouters (like our main api_router)
        if hasattr(route, "routes") and hasattr(route, "prefix"): # Check if it's a Mount or an APIRouter included directly
             # If route is an APIRouter instance itself (not a Mount of an APIRouter)
            if hasattr(route, "routes") and not hasattr(route, "app"): # Heuristic to differentiate APIRouter from Mount
                for sub_route in route.routes:
                    if hasattr(sub_route, "path"):
                        path = f"{route.prefix if hasattr(route, 'prefix') else ''}{sub_route.path}"
                        name = sub_route.name
                        methods = getattr(sub_route, 'methods', None)
                        logger.info(f"  Sub-Path: {path}, Name: {name}, Methods: {methods}")
            # If it's a Mount object which has an 'app' attribute that is the APIRouter
            elif hasattr(route, "app") and hasattr(route.app, "routes"):
                 for sub_route in route.app.routes:
                    if hasattr(sub_route, "path"):
                        path = f"{route.path}{sub_route.path}".replace("//","/") # route.path is the mount path
                        name = sub_route.name
                        methods = getattr(sub_route, 'methods', None)
                        logger.info(f"  Mounted Sub-Path: {path}, Name: {name}, Methods: {methods}")


    logger.info("--- END REGISTERED ROUTES ---")

except Exception as e: # Catch a more general exception if api_router itself is problematic
    logger.error(f"Error including main api_router or logging routes: {e}", exc_info=True)


# --- Root Endpoint ---
@app.get("/", tags=["Root"])
async def read_root():
    current_settings = get_settings()
    return {
        "message": f"Welcome to {current_settings.PROJECT_NAME} - Now with Dynamic Modules!",
        "environment": current_settings.ENVIRONMENT,
        "docs_url": app.docs_url,
        "api_base_prefix": current_settings.API_PREFIX
    }

logger.info(f"FastAPI application '{settings.PROJECT_NAME}' initialization complete.")
