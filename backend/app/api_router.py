# backend/app/api_router.py
from fastapi import APIRouter

# Import module-specific routers
from modules.health.v1 import endpoints as health_v1_endpoints
from modules.info.v1 import endpoints as info_v1_endpoints
from modules.ai_test.v1 import endpoints as ai_test_v1_endpoints # Ensure this import is added/correct

# Create the main API router - routers included here will be prefixed by /api from main.py
api_router = APIRouter()

# Include health module router
api_router.include_router(
    health_v1_endpoints.router,
    prefix="/health/v1"
    # Tags defined in endpoints
)

# Include info module router
api_router.include_router(
    info_v1_endpoints.router,
    prefix="/info/v1"
    # Tags defined in endpoints
)

# Include ai_test module router - ADDED
api_router.include_router(
    ai_test_v1_endpoints.router,
    prefix="/ai_test/v1"
    # Tags defined in endpoints
)

# Include future module routers here...