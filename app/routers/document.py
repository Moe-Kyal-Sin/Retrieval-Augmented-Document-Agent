from fastapi import File, UploadFile, HTTPException, APIRouter
import shutil
import uuid
import traceback
from fastapi import FastAPI

from app.core.config import UPLOAD_DIR
from app.core.store import DOCUMENT_STORE

from app.services.ingestion import IngestionAgent
from app.services.orchestrator import Orchestrator

router = APIRouter()

ingestion_agent = IngestionAgent()
orchestrator = Orchestrator()

@router.post("/uploadfile/")
async def upload(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code = 400, detail="No file uploaded")
    allowed_types = ['text/plain', 'application/pdf']
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail=f"Unsupported File Type. Only Txt and Pdf {file.content_type}")
    
    try:
        file_path = UPLOAD_DIR / file.filename
        with file_path.open("wb") as destinations:
            shutil.copyfileobj(file.file, destinations)

        result = ingestion_agent.run(file_path, file.content_type)

        document_id = str(uuid.uuid4())
        DOCUMENT_STORE[document_id] = {
            "document_id": document_id,
            "text": result['text'],
            "chunks": result['chunks'],
            "content_type": file.content_type,
            "filename": file.filename,
            "saved_path": file_path
            }

        
        return {"Message" : "File Uploaded Successfully",
                "DocumentId": document_id,
                "ContentType": file.content_type,
                "FileName": file.filename,
                "SavedPath": file_path,
                "TextLength": len(result['text']),
                "TextPreview": result['text'][:1000],
                "ChunksPreview": result['chunks'][:3]}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File cannot be saved {str(e)}")
    
    finally:
        file.file.close()

@router.post("/ask/")
async def ask_llm(document_id:str, question:str):

    try:

        document = DOCUMENT_STORE.get(document_id)
        if document is None:
            raise HTTPException(status_code=404, detail="Document not found")
        text = document['text']
        chunks = document['chunks']
        if not text:
            raise HTTPException(status_code = 400, detail="Canot Find the Document")
        if not question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        response = orchestrator.run(question, chunks)

        return {
            "Message" : "Successfully Generated a Response",
            "Response" : response,
        }
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))