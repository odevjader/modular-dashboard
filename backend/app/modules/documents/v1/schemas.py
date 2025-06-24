# v1/schemas.py for the documents module
from pydantic import BaseModel
from typing import Optional, List
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
