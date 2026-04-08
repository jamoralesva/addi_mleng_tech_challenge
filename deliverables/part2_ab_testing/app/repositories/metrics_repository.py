from typing import Any, Dict, List
from uuid import UUID


# Repository for storing experiment metrics - in-memory for demo purposes
# In a real implementation, this would interface with a database or analytics service
# or uses a Message Queue (like RabbitMQ or Kafka) or 
# at least a Background Task (FastAPI BackgroundTasks)
class MetricsRepository:
    def __init__(self):
        self._metrics: List[Dict[str, Any]] = []

    def save(self, 
             experiment_id: UUID, 
             user_id: str,
             variant_name: str,
             metric_key: str, 
             metric_value: float
        ) -> None:
        self._metrics.append({
            "experiment_id": experiment_id,
            "user_id": user_id,
            "variant_name": variant_name,
            "metric_key": metric_key,
            "metric_value": metric_value
        })

    def get_by_id(self, experiment_id: UUID) -> List[Dict[str, Any]]:
        return [
            m for m in self._metrics if m.get("experiment_id") == experiment_id
        ]
