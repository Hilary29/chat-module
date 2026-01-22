from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import get_settings


def get_llm() -> ChatGoogleGenerativeAI:
    """Retourne le LLM Google Gemini configure."""
    settings = get_settings()
    return ChatGoogleGenerativeAI(
        model=settings.gemini_model,
        temperature=settings.gemini_temperature,
        google_api_key=settings.google_api_key
    )
