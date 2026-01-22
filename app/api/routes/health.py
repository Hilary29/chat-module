from fastapi import APIRouter
from app.schemas.health import HealthCheckResponse, ServiceStatus
from app.core.vectorstore import VectorStoreManager
from app.config import get_settings
import httpx

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/", response_model=HealthCheckResponse)
async def health_check():
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

    overall_status = (
        ServiceStatus.HEALTHY
        if all(s == ServiceStatus.HEALTHY for s in services.values())
        else ServiceStatus.UNHEALTHY
    )

    return HealthCheckResponse(status=overall_status, services=services)
