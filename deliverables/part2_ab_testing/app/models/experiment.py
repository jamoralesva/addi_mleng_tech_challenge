import hashlib
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator


class ExperimentStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    ABORTED = "ABORTED"
    ARCHIVED = "ARCHIVED"


class Variant(BaseModel):
    name: str
    control: bool = False
    config: Optional[Dict[str, Any]] = {}
    traffic: float = Field(..., ge=0.0, le=1.0)


class Experiment(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    hypothesis: str
    description: Optional[str] = None
    is_feature_flag: bool = False
    status: ExperimentStatus = ExperimentStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.utcnow)
    variants: List[Variant]

    @field_validator('variants')
    @classmethod
    def validate_variants(cls, v: List[Variant]) -> List[Variant]:
        if len(v) < 2:
            raise ValueError('Must have at least two variants')
        control_count = sum(1 for variant in v if variant.control)
        if control_count != 1:
            raise ValueError('Must have exactly one control variant')
        traffic_sum = sum(variant.traffic for variant in v)
        if abs(traffic_sum - 1.0) > 1e-9:
            raise ValueError('Sum of traffic must be 1.0')
        # Check config consistency - all variants should have same keys as control
        control_variant = next(variant for variant in v if variant.control)
        control_keys = set(control_variant.config.keys())
        for variant in v:
            if set(variant.config.keys()) != control_keys:
                raise ValueError('All variants must have the same config keys as control')
        return v

    def assign_variant(self, user_id: str) -> Variant:
        assigner = ExperimentUserAssigner(self.variants)
        return assigner.assign_variant(user_id)


class ExperimentUserAssigner:
    def __init__(self, variants: List[Variant], epsilon: float = 1e-9):
        self.variants = variants
        self.total_traffic = sum(v.traffic for v in variants)
        
        if abs(self.total_traffic - 1.0) > epsilon:
            raise ValueError("the sum of traffic for all variants must be 1.0.")

        self.thresholds = []
        cumulative = 0.0
        for v in variants:
            cumulative += v.traffic
            self.thresholds.append((cumulative, v))

    def assign_variant(self, user_id: str) -> Variant:
        """
        Assigns a variant in a deterministic way using the user_id hash.
        """
        hash_object = hashlib.sha256(user_id.encode())
        hash_hex = hash_object.hexdigest()
        
        # using the first 8 digits
        hash_int = int(hash_hex[:8], 16)
        scale = hash_int / 0xFFFFFFFF  # norm to [0, 1)

        for threshold, variant in self.thresholds:
            if scale < threshold:
                return variant
        
        return self.variants[-1]