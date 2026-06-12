from pydantic_settings import BaseSettings , SettingsConfigDict
import os
class Settings(BaseSettings):

    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    CHROMA_PATH: str = os.getenv("CHROMA_PATH", "chroma_db")
    COLLECTION_NAME: str = os.getenv("COLLECTION_NAME", "langchain")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    MODELS_CACHE: str = os.getenv("MODELS_CACHE", "./models")
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "500"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "100"))
    RETRIEVAL_K: int = int(os.getenv("RETRIEVAL_K", "3"))
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "uploads")
    LOGS_DIR: str = os.getenv("LOGS_DIR", "logs")
    API_URL: str = os.getenv("API_URL", "http://localhost:8000")

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )
        
    
settings = Settings()