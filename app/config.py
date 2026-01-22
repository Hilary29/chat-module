from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Ollama
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "nomic-embed-text"

    # Google Gemini
    google_api_key: str = ""
    gemini_model: str = "gemini-3-flash-preview"
    gemini_temperature: float = 0.0

    # ChromaDB
    chroma_persist_directory: str = "./chroma_db"
    chroma_collection_name: str = "clientService_RAG"

    # RAG
    retriever_k: int = 2

    # Data
    excel_file_path: str = "./data/Modele_RAG_ServiceClient.xlsx"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
