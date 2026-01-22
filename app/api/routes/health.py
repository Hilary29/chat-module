from fastapi import APIRouter
from app.schemas.health import HealthCheckResponse, ReadinessResponse, ServiceStatus
from app.core.vectorstore import VectorStoreManager
from app.config import get_settings
import httpx

router = APIRouter(prefix="/health", tags=["Health"])

API_VERSION = "1.0.0"


@router.get(
    "/",
    response_model=HealthCheckResponse,
    summary="Health check",
    description="Verifie l'etat de sante global du service"
)
async def health_check():
    """Verifie l'etat de sante des services."""
    settings = get_settings()
    services = {}

    # Verifier Ollama
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.ollama_base_url}/api/tags",
                timeout=5.0
            )
            services["ollama"] = (
                ServiceStatus.HEALTHY if response.status_code == 200
                else ServiceStatus.UNHEALTHY
            )
    except Exception:
        services["ollama"] = ServiceStatus.UNHEALTHY

    # Verifier ChromaDB
    try:
        VectorStoreManager.get_vectorstore()
        services["chromadb"] = ServiceStatus.HEALTHY
    except Exception:
        services["chromadb"] = ServiceStatus.UNHEALTHY

    # Statut global
    if all(s == ServiceStatus.HEALTHY for s in services.values()):
        overall_status = ServiceStatus.HEALTHY
    elif any(s == ServiceStatus.HEALTHY for s in services.values()):
        overall_status = ServiceStatus.DEGRADED
    else:
        overall_status = ServiceStatus.UNHEALTHY

    return HealthCheckResponse(
        status=overall_status,
        version=API_VERSION,
        services=services
    )


@router.get(
    "/ready",
    response_model=ReadinessResponse,
    summary="Readiness check",
    description="Verifie si le service est pret a recevoir du trafic"
)
async def readiness_check():
    """Verifie si tous les composants sont initialises."""
    settings = get_settings()

    # Verifier vectorstore
    try:
        VectorStoreManager.get_vectorstore()
        vectorstore_loaded = True
    except Exception:
        vectorstore_loaded = False

    # Verifier Ollama/embeddings
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.ollama_base_url}/api/tags",
                timeout=5.0
            )
            embeddings_available = response.status_code == 200
    except Exception:
        embeddings_available = False

    # Verifier Google API Key
    llm_available = bool(settings.google_api_key)

    ready = all([vectorstore_loaded, llm_available, embeddings_available])

    return ReadinessResponse(
        ready=ready,
        vectorstore_loaded=vectorstore_loaded,
        llm_available=llm_available,
        embeddings_available=embeddings_available
    )


@router.get("/live", summary="Liveness check")
async def liveness_check():
    """Simple liveness probe pour Kubernetes."""
    return {"status": "alive"}
