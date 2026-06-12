import os
os.environ["HF_HUB_OFFLINE"] = "1" 

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from app.core.logger import get_logger
from app.core.config import settings
import chromadb

logger = get_logger("chroma_db")

embedding_model = HuggingFaceEmbeddings(
    model_name = settings.EMBEDDING_MODEL,
    model_kwargs = {"device": "cpu"},
    cache_folder = settings.MODELS_CACHE
)

chromadb_client = chromadb.PersistentClient(path = settings.CHROMA_PATH)
def create_vector_store(chunks):
    logger.info(f"Storing {len(chunks)} chunks in vector store")
    vector_db = Chroma.from_documents(
        documents = chunks,
        embedding = embedding_model,
        client = chromadb_client,
        collection_name = settings.COLLECTION_NAME   
    )
    logger.info(f"Chunks stored successfully")
    return vector_db

