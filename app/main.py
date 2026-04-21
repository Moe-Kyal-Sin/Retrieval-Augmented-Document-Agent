from fastapi import FastAPI, File, UploadFile, HTTPException
import shutil
import uuid
import traceback
from fastapi import FastAPI

from app.core.config import UPLOAD_DIR
from app.core.store import DOCUMENT_STORE
from app.routers.document import router as document_router

from app.services.ingestion import IngestionAgent
from app.services.orchestrator import Orchestrator

app = FastAPI()
app.include_router(document_router)

ingestion_agent = IngestionAgent()
orchestrator = Orchestrator()

@app.get("/")
async def root():
    return {"message": "Backed is running"}


