# backend/app/modules/info/v1/endpoints.py
from fastapi import APIRouter
# --- IMPORT CORRIGIDO ---
from app.core.config import settings # Import settings using absolute path from app package
# --- FIM IMPORT CORRIGIDO ---
from .schemas import SystemInfoResponse # Import the response schema (relative import is OK here)
import datetime

# Define the router for this module (info) and version (v1)
router = APIRouter()

@router.get("/status", response_model=SystemInfoResponse, tags=["Info"]) # Updated Tag
async def get_system_status():
    """
    Retrieves basic system status information.
    (Will be accessible at /api/info/v1/status)
    """
    # Ensure settings is loaded
    if not settings:
         # This should ideally not happen if config is loaded correctly at startup
         return SystemInfoResponse(environment="unknown", project_name="unknown", server_time_utc=datetime.datetime.now(datetime.timezone.utc), api_prefix="/api")

    return SystemInfoResponse(
        environment=settings.ENVIRONMENT,
        project_name=settings.PROJECT_NAME,
        server_time_utc=datetime.datetime.now(datetime.timezone.utc),
        api_prefix=settings.API_PREFIX
    )