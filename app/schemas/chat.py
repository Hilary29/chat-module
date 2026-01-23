from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional


class IntentType(str, Enum):
    #Types d'intention detectes par le chatbot
    GREETING = "greeting"
    SERVICE_CLIENT = "service_client"
    OTHER = "other"


class ChatRequest(BaseModel):
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
    content: str = Field(..., description="Contenu du document")
    category: Optional[str] = Field(None, description="Categorie du document")
    intent: Optional[str] = Field(None, description="Intention detectee")


class ChatResponse(BaseModel):
    answer: str = Field(..., description="Reponse du chatbot")
    intent: IntentType = Field(..., description="Intention detectee")
    sources: Optional[List[SourceDocument]] = Field(
        default=None,
        description="Documents sources utilises"
    )


class ErrorResponse(BaseModel):
    error: str = Field(..., description="Message d'erreur")
    detail: Optional[str] = Field(None, description="Details supplementaires")
