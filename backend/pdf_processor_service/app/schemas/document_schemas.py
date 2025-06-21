from pydantic import BaseModel
from datetime import datetime
from typing import List

class DocumentChunkBase(BaseModel):
    chunk_text: str
    chunk_order: int

class DocumentChunkResponse(DocumentChunkBase):
    id: int
    document_id: int
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        orm_mode = True # For Pydantic V1, or from_attributes = True for V2

class DocumentBase(BaseModel):
    file_hash: str
    file_name: str | None = None

class DocumentCreate(DocumentBase):
    pass

class DocumentResponse(DocumentBase):
    id: int
    created_at: datetime
    updated_at: datetime | None = None
    # Optional: include chunks in response, can be heavy
    # chunks: List[DocumentChunkResponse] = []

    class Config:
        orm_mode = True # For Pydantic V1, or from_attributes = True for V2
