# schemas.py for the documents module
from pydantic import BaseModel
from typing import Optional, List, Any

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

# Schemas for Task Status
class TaskStatusErrorInfo(BaseModel):
    error: Optional[str] = None
    traceback: Optional[str] = None

class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    result: Optional[Any] = None # Using Any for flexibility in what 'result' might contain
    error_info: Optional[TaskStatusErrorInfo] = None
    # message: Optional[str] = None # Example if the transcriber returns a top-level message
