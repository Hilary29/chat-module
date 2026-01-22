from pydantic import BaseModel, Field
from typing import Dict
from enum import Enum


class ServiceStatus(str, Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    DEGRADED = "degraded"


class HealthCheckResponse(BaseModel):
    """Schema pour le health check."""
    status: ServiceStatus = Field(..., description="Statut global du service")
    version: str = Field(..., description="Version de l'API")
    services: Dict[str, ServiceStatus] = Field(
        ...,
        description="Statut des services dependants"
    )


class ReadinessResponse(BaseModel):
    """Schema pour le readiness check."""
    ready: bool = Field(..., description="Le service est-il pret ?")
    vectorstore_loaded: bool = Field(..., description="ChromaDB charge ?")
    llm_available: bool = Field(..., description="LLM disponible ?")
    embeddings_available: bool = Field(..., description="Embeddings disponibles ?")
