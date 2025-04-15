# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers directly
# Make sure the path is relative to the 'app' directory where main.py resides
from api.health.v1 import endpoints as health_v1_endpoints
# Import other module routers here later

from core.config import settings, logger # Use logger from config

# --- FastAPI App Initialization ---
# Conditionally set docs/redoc/openapi URLs based on environment
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
# Ensure BACKEND_CORS_ORIGINS is correctly processed from List[Union[AnyHttpUrl, str]]
allow_origins = []
if settings.BACKEND_CORS_ORIGINS:
    for origin in settings.BACKEND_CORS_ORIGINS:
        if isinstance(origin, str):
            allow_origins.append(origin.strip())
        else: # Assuming AnyHttpUrl
            allow_origins.append(str(origin)) # Convert AnyHttpUrl to string

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
# Include the v1 health router with its full path prefix
logger.info(f"Including Health v1 router at prefix: {settings.API_PREFIX}/health/v1")
app.include_router(
    health_v1_endpoints.router,
    prefix=f"{settings.API_PREFIX}/health/v1",
    # tags are defined within the router itself in endpoints.py
)
# Include other routers here later


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