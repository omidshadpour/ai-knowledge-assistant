from fastapi import APIRouter , UploadFile , File
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.services.rag import ask_question , ask_question_stream , extract_sources
from app.services.ingestion import process_pdf
from app.services.retrieval import retrieve_documents
from app.core.logger import get_logger
from app.core.config import settings
import asyncio  
import os
import uuid

logger = get_logger("routes")
router = APIRouter()

@router.get("/")
def home():
    return {"message": "Professional RAG API Running"}

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    logger.info(f"Uploading file: {file.filename}")
    os.makedirs(settings.UPLOAD_DIR  , exist_ok=True)

    filename = f"{uuid.uuid4()}.pdf"
    pdf_path = os.path.join(settings.UPLOAD_DIR, filename)

    file_bytes = await file.read()

    with open(pdf_path , "wb") as f:
        f.write(file_bytes)

    logger.info(f"File saved: {pdf_path}")
    document_id = await asyncio.to_thread(process_pdf , pdf_path)
    logger.info(f"File processed, document_id: {document_id}")
    
    return {
        "filename": file.filename,
        "stored_filename": filename,
        "document_id" : document_id
    }


class QuestionRequest(BaseModel):
    question: str
    document_id: str
    session_id: str

@router.post("/ask")
async def ask(request: QuestionRequest):
    logger.info(f"Question: {request.question[:50]}, document_id: {request.document_id} ")
    answer = ask_question(
        request.question,
        request.document_id,
        request.session_id
    )
    
    return answer

@router.post("/ask-stream")
async def ask_stream(request: QuestionRequest):
    logger.info(f"Stream question: '{request.question[:50]}', document_id: {request.document_id}")

    def generate():
        for token in ask_question_stream(
            request.question,
            request.document_id,
            request.session_id
        ):
            yield token

        
    return StreamingResponse(generate() , media_type="text/plain")

@router.post("/ask-sources")
async def ask_sources(request: QuestionRequest):
    logger.info(f"Getting sources for: '{request.question[:50]}'")

    docs = retrieve_documents(request.question , request.document_id)
    sources = extract_sources(docs)
    return {"sources": sources}