# backend/app/modules/info/v1/endpoints.py
from fastapi import APIRouter
from core.config import settings # Import settings from core
from .schemas import SystemInfoResponse # Import the response schema
import datetime

# Define the router for this module (info) and version (v1)
router = APIRouter()

@router.get("/status", response_model=SystemInfoResponse, tags=["Info v1"])
async def get_system_status():
    """
    Retrieves basic system status information.
    (Will be accessible at /api/info/v1/status)
    """
    return SystemInfoResponse(
        environment=settings.ENVIRONMENT,
        project_name=settings.PROJECT_NAME,
        server_time_utc=datetime.datetime.now(datetime.timezone.utc),
        api_prefix=settings.API_PREFIX
    )