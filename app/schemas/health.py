from pydantic import BaseModel, Field
from typing import Dict
from enum import Enum


class ServiceStatus(str, Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"


class HealthCheckResponse(BaseModel):
    status: ServiceStatus = Field(..., description="Statut global du service")
    services: Dict[str, ServiceStatus] = Field(
        ...,
        description="Statut des services dependants"
    )
