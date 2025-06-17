from fastapi import APIRouter
from .schemas import PingResponse

router = APIRouter()

@router.get("/ping", response_model=PingResponse, tags=["Documents V1"])
async def ping_documents():
    return {"message": "Pong from Documents v1"}
