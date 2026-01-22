from langchain_ollama import OllamaEmbeddings
from app.config import get_settings


def get_embedding_function() -> OllamaEmbeddings:
    """Retourne la fonction d'embedding Ollama configuree."""
    settings = get_settings()
    return OllamaEmbeddings(
        model=settings.ollama_model,
        base_url=settings.ollama_base_url
    )
