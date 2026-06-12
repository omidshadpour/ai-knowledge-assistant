from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.vector_store.chroma_db import create_vector_store
from app.core.exceptions import PDFProcessingError , VectorStoreError
from app.core.logger import get_logger
from app.core.config import settings
import uuid


logger = get_logger("ingestion")

def load_pdf(pdf_path : str):

    try:
        logger.info(f"Loading PDF: {pdf_path}")
        loader = PyPDFLoader(pdf_path)
        document = loader.load()
        logger.info(f"PDF loaded successfully: {len(document)} pages")

        return document
    except Exception as e:
        logger.error(f"Failed to load PDF: {str(e)}")
        raise PDFProcessingError(f"Could not read PDF: {str(e)}")


def create_chunks(document):
    chunks = RecursiveCharacterTextSplitter(
        chunk_size = settings.CHUNK_SIZE,   
        chunk_overlap = settings.CHUNK_OVERLAP
    ).split_documents(document)

    logger.debug(f"Created {len(chunks)} chunks")
    return chunks

def process_pdf(pdf_path : str):
    
    try:
        document_id = str(uuid.uuid4())
        logger.info(f"Processing PDF , document_id: {document_id}")

        documents = load_pdf(pdf_path)
        chunks = create_chunks(documents)

        for chunk in chunks:
            chunk.metadata["document_id"] = document_id
            chunk.metadata["source"] = pdf_path

        create_vector_store(chunks)
        logger.info(f"PDF processed successfully , document_id: {document_id}")
        return document_id

    except Exception as e:
        logger.error(f"Unexpected error processing PDF: {str(e)}")
        raise VectorStoreError(f"Failed to store document: {str(e)}")