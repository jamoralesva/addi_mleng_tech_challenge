from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from ..models.experiment import ExperimentStatus, Variant


class ExperimentSpec(BaseModel):
    name: str
    hypothesis: str
    description: Optional[str] = None
    is_feature_flag: Optional[bool] = False
    variants: List[Variant] = Field(..., min_items=2)


class ExperimentResponse(BaseModel):
    id: UUID
    name: str
    hypothesis: str
    description: Optional[str] = None
    status: ExperimentStatus
    created_at: datetime
    variants: List[Variant]


class ExperimentUpdate(BaseModel):
    tags: Optional[List[str]] = None
    status: Optional[ExperimentStatus] = None


class MetricValue(BaseModel):
    metric_key: str
    value: float
    timestamp: datetime