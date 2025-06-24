# v1/schemas.py for the documents module
from pydantic import BaseModel
from typing import Optional, List, Any # Added Any
from datetime import datetime

class PingResponse(BaseModel):
    message: str

# Schema for reading a single document chunk
class DocumentChunkRead(BaseModel):
    id: int
    document_id: int
    chunk_text: str
    chunk_order: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Schema for reading a document, including its chunks
class DocumentRead(BaseModel):
    id: int
    file_hash: str
    file_name: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    chunks: List[DocumentChunkRead] = []

    class Config:
        from_attributes = True

# Schema for paginated list of documents
class DocumentListResponse(BaseModel):
    items: List[DocumentRead]
    total: int
    page: int
    size: int
    pages: int

# --- Schemas moved from top-level documents/schemas.py ---

class DocumentBase(BaseModel):
    filename: str
    content_type: Optional[str] = None
    size: Optional[int] = None

class DocumentCreate(DocumentBase):
    pass

class Document(DocumentBase): # This might be a duplicate or needs renaming if DocumentRead is preferred
    id: int

    class Config:
        from_attributes = True

# Schemas for Task Status
class TaskStatusErrorInfo(BaseModel):
    error: Optional[str] = None
    traceback: Optional[str] = None

class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    result: Optional[Any] = None
    error_info: Optional[TaskStatusErrorInfo] = None

# Schema for Document Query Request (used in v1/endpoints.py)
class DocumentQueryRequest(BaseModel):
    user_query: str

# Schema for the response from the transcriber service part
class TranscriberDataResponse(BaseModel):
    task_id: str
    document_id: int # Added this as per transcritor-pdf/src/main.py response
    message: str

# Schema for the overall /upload endpoint response from the gateway
class GatewayDocumentUploadResponse(BaseModel):
    message: str
    transcriber_data: TranscriberDataResponse
    original_filename: str
    uploader_user_id: int # Assuming user_id is int

# Schema for the data part of the transcriber's query response
class TranscriberQueryData(BaseModel):
    document_id: str
    query: str
    answer: str

# Schema for the overall /query/{document_id} endpoint response from the gateway
class GatewayDocumentQueryResponse(BaseModel):
    message: str
    transcriber_data: TranscriberQueryData
    original_document_id: str
    queried_by_user_id: int
