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
