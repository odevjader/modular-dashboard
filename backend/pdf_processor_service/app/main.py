from fastapi import FastAPI
from .routers import processing_router # Assuming processing_router.py is in app/routers/

app = FastAPI(title="PDF Processor Service")

app.include_router(processing_router.router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}
