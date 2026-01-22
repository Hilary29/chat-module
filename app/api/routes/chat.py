from fastapi import APIRouter, HTTPException
from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
    ChatResponseWithSources,
    SourceDocument,
    ErrorResponse
)
from app.core.rag_pipeline import get_rag_pipeline
from datetime import datetime
import logging

router = APIRouter(prefix="/chat", tags=["Chat"])
logger = logging.getLogger(__name__)


@router.post(
    "/",
    response_model=ChatResponse,
    responses={
        200: {"description": "Reponse du chatbot"},
        500: {"model": ErrorResponse, "description": "Erreur interne"}
    },
)
async def ask_question(request: ChatRequest):
    #Endpoint pour poser une question
    try:
        pipeline = get_rag_pipeline()

        if request.include_sources:
            result = pipeline.ask(request.question)
            sources = [
                SourceDocument(
                    content=src["content"],
                    category=src["metadata"].get("category"),
                    intent=src["metadata"].get("intent")
                )
                for src in result["sources"]
            ]
            return ChatResponseWithSources(
                answer=result["answer"],
                sources=sources,
                timestamp=datetime.utcnow()
            )
        else:
            answer = pipeline.ask_simple(request.question)
            return ChatResponse(
                answer=answer,
                timestamp=datetime.utcnow()
            )

    except Exception as e:
        logger.error(f"Erreur lors du traitement de la question: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors du traitement: {str(e)}"
        )
