# backend/app/api/health/v1/endpoints.py
from fastapi import APIRouter
from pydantic import BaseModel

# Define the router for this specific module (health) and version (v1)
router = APIRouter()

class HealthResponse(BaseModel):
    status: str = "ok"
    message: str = "API health module v1 is active"

# Define routes relative to the prefix this router will be included with
@router.get("/health", response_model=HealthResponse, tags=["Health v1"])
async def health_check():
    """
    Checks if the health module v1 is running.
    (Will be accessible at /api/health/v1/health)
    """
    return HealthResponse()

# You could add other v1 health-related endpoints here later