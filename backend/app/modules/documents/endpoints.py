from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from app.core.dependencies import get_current_active_user
from app.models.user import User
from . import services
from .v1 import endpoints as v1_endpoints
from pydantic import BaseModel
from .schemas import TaskStatusResponse # Import the new response model

# New imports for the gateway endpoint
import httpx
from fastapi import Request
from typing import Any
from app.core.config import settings # For PDF_PROCESSOR_SERVICE_URL


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

@api_router.get(
    "/upload/status/{task_id}",
    response_model=TaskStatusResponse,
    summary="Get document processing status from gateway",
    tags=["Documents Module"]
)
async def get_document_upload_status_gateway(
    task_id: str,
    current_user: User = Depends(get_current_active_user) # Protect endpoint
):
    # current_user is not explicitly passed to the service now, but good for auth.
    return await services.get_document_processing_status(task_id)


@api_router.post("/upload-and-process", response_model=Any, summary="Upload PDF and trigger processing via microservice", tags=["Documents Module"])
async def upload_and_process_document(
    request: Request, # To construct absolute URLs if needed, or for logging
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user) # Protect the endpoint
):
    if not file.content_type == "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDFs are accepted.")

    pdf_processor_url = f"{settings.PDF_PROCESSOR_SERVICE_URL}/processing/process-pdf"

    async with httpx.AsyncClient() as client:
        try:
            # Prepare files for streaming upload to the microservice
            files = {'file': (file.filename, await file.read(), file.content_type)}
            response = await client.post(pdf_processor_url, files=files, timeout=30.0) # Increased timeout

            response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
            return response.json() # Return the JSON response from the microservice
        except httpx.HTTPStatusError as e:
            # Attempt to forward the error detail from the microservice if possible
            error_detail = "Error processing document." # Default error
            if e.response and e.response.content:
                try:
                    error_detail = e.response.json().get("detail", error_detail)
                except Exception: # Gracefully handle if response is not JSON or detail is not present
                    pass
            raise HTTPException(status_code=e.response.status_code if e.response else 500, detail=error_detail)
        except httpx.RequestError as e:
            # Network error or other request issue
            raise HTTPException(status_code=503, detail=f"Service unavailable: Error connecting to PDF Processor. {str(e)}")
        except Exception as e:
            # Catch-all for other unexpected errors
            # Log e here for debugging
            # Modified for debugging to see the actual error string
            raise HTTPException(status_code=500, detail=f"Unexpected error in endpoint: {type(e).__name__} - {str(e)}")
