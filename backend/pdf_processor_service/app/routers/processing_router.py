from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from .. import schemas, services, models # Updated to include models for potential direct use if needed
from ..core.database import get_db

router = APIRouter(
    prefix="/processing",
    tags=["Processing"],
)

@router.post("/process-pdf", response_model=schemas.DocumentResponse)
async def process_pdf_endpoint(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.content_type == "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDFs are accepted.")

    file_contents = await file.read()
    if not file_contents:
        raise HTTPException(status_code=400, detail="Empty file uploaded.")

    try:
        # The service function from TASK-050 will handle document creation and chunking
        document = services.create_document_and_chunks(
            db=db,
            file_contents=file_contents,
            original_file_name=file.filename
        )
        return document
    except Exception as e:
        # Log the exception e here in a real application
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")
