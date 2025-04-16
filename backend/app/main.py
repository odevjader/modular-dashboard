# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers directly from their module locations
from modules.health.v1 import endpoints as health_v1_endpoints
from modules.info.v1 import endpoints as info_v1_endpoints # ADDED IMPORT

from core.config import settings, logger

# --- FastAPI App Initialization ---
openapi_url = f"{settings.API_PREFIX}/openapi.json" if settings.ENVIRONMENT == "development" else None
docs_url = "/docs" if settings.ENVIRONMENT == "development" else None
redoc_url = "/redoc" if settings.ENVIRONMENT == "development" else None

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
    allow_origins = [str(origin).strip() for origin in settings.BACKEND_CORS_ORIGINS if origin]

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


# --- Include Module Routers ---
# Health module
logger.info(f"Including Health v1 router at prefix: {settings.API_PREFIX}/health/v1")
app.include_router(
    health_v1_endpoints.router,
    prefix=f"{settings.API_PREFIX}/health/v1"
)
# Info module - ADDED ROUTER INCLUDE
logger.info(f"Including Info v1 router at prefix: {settings.API_PREFIX}/info/v1")
app.include_router(
    info_v1_endpoints.router,
    prefix=f"{settings.API_PREFIX}/info/v1"
)


# --- Root Endpoint ---
@app.get("/", tags=["Root"])
async def read_root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "environment": settings.ENVIRONMENT,
        "docs_url": app.docs_url,
        "api_base_prefix": settings.API_PREFIX
    }

logger.info(f"FastAPI application '{settings.PROJECT_NAME}' initialization complete.")