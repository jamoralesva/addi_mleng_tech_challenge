from datetime import datetime

from fastapi import FastAPI, status
from pydantic import BaseModel

from source.application.graph import workflow
from source.application.state import GraphState

app = FastAPI(
    title="ML Ops Challenge API",
    description="Servicio de inferencia basado en LangGraph",
    version="1.0.0"
)

class HealthCheck(BaseModel):
    status: str
    timestamp: datetime
    version: str

@app.get(
    "/health",
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

# Entry point para debugging local
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)