from typing import Dict, List, Optional
from uuid import UUID

from ..models.experiment import Experiment, ExperimentStatus


class ExperimentRepository:
    def __init__(self):
        self._experiments: Dict[UUID, Experiment] = {}

    def save(self, experiment: Experiment) -> Experiment:
        self._experiments[experiment.id] = experiment
        return experiment

    def get_by_id(self, experiment_id: UUID) -> Optional[Experiment]:
        return self._experiments.get(experiment_id)

    def get_all(self, include_archived: bool = False) -> List[Experiment]:
        if include_archived:
            return list(self._experiments.values())
        return [exp for exp in self._experiments.values() if exp.status != ExperimentStatus.ARCHIVED]

    def update(self, experiment: Experiment) -> Experiment:
        if experiment.id not in self._experiments:
            raise ValueError("Experiment not found")
        self._experiments[experiment.id] = experiment
        return experiment

    def delete(self, experiment_id: UUID) -> None:
        if experiment_id in self._experiments:
            del self._experiments[experiment_id]