from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class ChatRequest(BaseModel):
    #Schema pour une requete de chat
    question: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="La question a poser au chatbot"
    )
    include_sources: bool = Field(
        default=False,
        description="Inclure les sources utilisees pour la reponse"
    )


class SourceDocument(BaseModel):
    #Schema pour un document source.
    content: str = Field(..., description="Contenu du document")
    category: Optional[str] = Field(None, description="Categorie du document")
    intent: Optional[str] = Field(None, description="Intention detectee")


class ChatResponse(BaseModel):
    #Schema pour une reponse de chat simple
    answer: str = Field(..., description="Reponse du chatbot")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Horodatage de la reponse"
    )


class ChatResponseWithSources(ChatResponse):
    """Schema pour une reponse de chat avec sources."""
    sources: List[SourceDocument] = Field(
        default=[],
        description="Documents sources utilises"
    )


class ErrorResponse(BaseModel):
    """Schema pour les erreurs."""
    error: str = Field(..., description="Message d'erreur")
    detail: Optional[str] = Field(None, description="Details supplementaires")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
