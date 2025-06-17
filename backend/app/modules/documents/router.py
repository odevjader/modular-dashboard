from fastapi import APIRouter, Depends, UploadFile, File
from app.core.dependencies import get_current_active_user
from app.models.user import User
from . import services
from .v1 import endpoints as v1_endpoints

api_router = APIRouter()

# Include v1 routes
api_router.include_router(v1_endpoints.router, prefix="/v1")

# You can add module-wide routes here if needed, or just use v1 for now
@api_router.get("/", tags=["Documents Module"])
async def read_documents_root():
    return {"message": "Welcome to the Documents Module"}

@api_router.post("/upload", summary="Upload a document for processing", tags=["Documents Module"])
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user)
):
    # Placeholder for service call
    # result = await services.handle_file_upload(file, current_user)
    # return {"filename": file.filename, "message": "File uploaded successfully", "detail": result}
    # For now, just return a placeholder response until the service is implemented
    return await services.handle_file_upload(file, current_user.id) # Pass user_id for now
