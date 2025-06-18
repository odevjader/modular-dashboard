from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from app.core.dependencies import get_current_active_user
from app.models.user import User
from . import services
from .v1 import endpoints as v1_endpoints
from pydantic import BaseModel # Add this import

api_router = APIRouter()

class DocumentQueryRequest(BaseModel):
    user_query: str

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

@api_router.post("/query/{document_id}", summary="Query a processed document via gateway", tags=["Documents Module"])
async def query_document_gateway(
    document_id: str,
    request_data: DocumentQueryRequest, # Use the new Pydantic model
    current_user: User = Depends(get_current_active_user)
):
    if not request_data.user_query:
        raise HTTPException(status_code=400, detail="User query cannot be empty.")
    return await services.handle_document_query(document_id, request_data.user_query, current_user.id)
