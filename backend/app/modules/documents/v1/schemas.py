# v1/schemas.py for the documents module
from pydantic import BaseModel
from typing import Optional, List

class PingResponse(BaseModel):
    message: str
