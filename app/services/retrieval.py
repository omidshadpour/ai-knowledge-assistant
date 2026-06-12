from langchain_chroma import Chroma
from app.vector_store.chroma_db import embedding_model , chromadb_client
from app.core.logger import get_logger
from app.core.config import settings

logger = get_logger("retrieval")

def get_vector_db():
    return Chroma(
        embedding_function = embedding_model,
        client = chromadb_client,
         collection_name = settings.COLLECTION_NAME
    )


def retrieve_documents(question : str , document_id : str):
    logger.info(f"Retriving documents for question: '{question[:50]}...'")
    vector_db = get_vector_db()
    results = vector_db.similarity_search(
        question,
        k = settings.RETRIEVAL_K ,
        filter = {
            "document_id" : document_id
        }
    )
    logger.debug(f"Found {len(results)} documents")
    return results
