from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.api.routes import chat, health
from app.core.document_loader import load_excel_as_documents
from app.core.vectorstore import VectorStoreManager
from app.config import get_settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Demarrage de l'application...")
    settings = get_settings()

    try:
        logger.info(f"Chargement des documents depuis {settings.excel_file_path}")
        documents = load_excel_as_documents(settings.excel_file_path)
        logger.info(f"{len(documents)} documents charges")

        logger.info("Initialisation de ChromaDB...")
        VectorStoreManager.get_vectorstore(documents=documents)
        logger.info("ChromaDB initialise avec succes")

    except Exception as e:
        logger.error(f"Erreur lors de l'initialisation: {e}")
        raise

    yield

    logger.info("Arret de l'application...")


app = FastAPI(
    title="Service Client RAG Chatbot API",
    description="API REST pour le chatbot RAG du service client.",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api/v1")
app.include_router(health.router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)
