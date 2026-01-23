from fastapi import APIRouter, HTTPException
from app.schemas.chat import ChatRequest, ChatResponse, SourceDocument, ErrorResponse, IntentType
from app.core.rag_pipeline import get_rag_pipeline
import logging

router = APIRouter(prefix="/chat", tags=["Chat"])
logger = logging.getLogger(__name__)


@router.post(
    "/",
    response_model=ChatResponse,
    responses={500: {"model": ErrorResponse, "description": "Erreur interne"}},
)
async def ask_question(request: ChatRequest):
    try:
        pipeline = get_rag_pipeline()
        result = pipeline.ask(request.question)

        sources = None
        if request.include_sources:
            sources = [
                SourceDocument(
                    content=src["content"],
                    category=src["metadata"].get("category"),
                )
                for src in result["sources"]
            ]

        return ChatResponse(
            answer=result["answer"],
            intent=IntentType(result["intent"]),
            sources=sources
        )

    except Exception as e:
        logger.error(f"Erreur lors du traitement de la question: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors du traitement: {str(e)}"
        )
