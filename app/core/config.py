from pydantic_settings import BaseSettings , SettingsConfigDict

class Settings(BaseSettings):

    # Groq Setting
    GROQ_API_KEY: str
    GROQ_MODEL: str

    # Vector Store Setting
    CHROMA_PATH: str
    COLLECTION_NAME: str
    EMBEDDING_MODEL: str
    MODELS_CACHE: str
    
    # Ingestion Setting
    CHUNK_SIZE : int
    CHUNK_OVERLAP : int
    RETRIEVAL_K : int

    # Paths
    UPLOAD_DIR : str
    LOGS_DIR : str

    # Streamlit
    API_URL : str

    model_config = SettingsConfigDict(
        env_file = ".env",
        extra = "ignore"
    )
        
    
settings = Settings()