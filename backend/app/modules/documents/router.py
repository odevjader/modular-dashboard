from fastapi import APIRouter
from .v1 import endpoints as v1_endpoints

api_router = APIRouter()

# Include v1 routes
api_router.include_router(v1_endpoints.router, prefix="/v1")

# You can add module-wide routes here if needed, or just use v1 for now
@api_router.get("/", tags=["Documents Module"])
async def read_documents_root():
    return {"message": "Welcome to the Documents Module"}
