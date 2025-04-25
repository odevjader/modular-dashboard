# backend/app/api_router.py
from fastapi import APIRouter

# Import module-specific routers
from app.modules.health.v1 import endpoints as health_v1_endpoints
from app.modules.info.v1 import endpoints as info_v1_endpoints
from app.modules.ai_test.v1 import endpoints as ai_test_v1_endpoints
from app.modules.gerador_quesitos.v1 import endpoints as gerador_quesitos_v1_endpoints
from app.core_modules.auth.v1 import endpoints as auth_v1_endpoints # Import correto

# Create the main API router - routers included here will be prefixed by /api from main.py
api_router = APIRouter()

# --- Includes ---
api_router.include_router(
    health_v1_endpoints.router,
    prefix="/health/v1",
    tags=["Health"]
)
api_router.include_router(
    info_v1_endpoints.router,
    prefix="/info/v1",
    tags=["Info"]
)
api_router.include_router(
    ai_test_v1_endpoints.router,
    prefix="/ai_test/v1",
    tags=["AI Test"]
)
api_router.include_router(
    gerador_quesitos_v1_endpoints.router,
    prefix="/gerador_quesitos/v1",
    tags=["Gerador Quesitos"]
)
api_router.include_router(
    auth_v1_endpoints.router,
    # --- PREFIX CORRIGIDO ---
    prefix="/auth/v1", # Adicionado /v1 para consistência
    tags=["Authentication"]
)