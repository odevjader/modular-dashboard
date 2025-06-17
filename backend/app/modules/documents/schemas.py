# schemas.py for the documents module
from pydantic import BaseModel
from typing import Optional, List

class DocumentBase(BaseModel):
    filename: str
    content_type: Optional[str] = None
    size: Optional[int] = None

class DocumentCreate(DocumentBase):
    pass

class Document(DocumentBase):
    id: int # Assuming an ID will be assigned upon storage

    class Config:
        orm_mode = True
