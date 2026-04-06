
from datetime import datetime

from fastapi import APIRouter, status
from pydantic import BaseModel

router = APIRouter(
    prefix="/health",
    tags=["system health"],
    responses={404: {"description": "Not found"}},
)

class HealthCheck(BaseModel):
    status: str
    timestamp: datetime
    version: str

@router.get(
    "/",
    tags=["system"],
    summary="Check health of the service",
    response_model=HealthCheck,
    status_code=status.HTTP_200_OK
)
async def get_health():
    """
    Endpoint para monitoreo y Liveness/Readiness probes.
    """
    return HealthCheck(
        status="OK",
        timestamp=datetime.now(),
        version="1.0.0"
    )