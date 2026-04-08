from uuid import UUID

from fastapi import APIRouter, HTTPException, Query

from ....models.experiment import Experiment, ExperimentStatus
from ....repositories.experiment_repository import ExperimentRepository
from ....repositories.metrics_repository import MetricsRepository
from ....schemas.experiment import (
    ExperimentResponse,
    ExperimentSpec,
    ExperimentUpdate,
    MetricValue,
    Variant,
)

router = APIRouter()
repo = ExperimentRepository()  # In-memory for demo
metrics_repo = MetricsRepository()  # In-memory for demo

@router.post("/experiment", response_model=ExperimentResponse, status_code=201)
async def create_experiment(experiment_spec: ExperimentSpec) -> ExperimentResponse:
    try:
        experiment = Experiment(
            name=experiment_spec.name,
            hypothesis=experiment_spec.hypothesis,
            description=experiment_spec.description,
            is_feature_flag=experiment_spec.is_feature_flag,
            variants=experiment_spec.variants
        )
        saved = repo.save(experiment)
        return ExperimentResponse(
            id=saved.id,
            name=saved.name,
            hypothesis=saved.hypothesis,
            description=saved.description,
            status=saved.status,
            created_at=saved.created_at,
            variants=saved.variants
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/experiment/{experiment_id}", response_model=ExperimentResponse)
async def get_experiment(
    experiment_id: UUID, 
    include_archive: bool = Query(False, alias="include-archive")
    ) -> ExperimentResponse:
    experiment = repo.get_by_id(experiment_id)
    if not experiment or (experiment.status == ExperimentStatus.ARCHIVED and not include_archive):
        raise HTTPException(status_code=404, detail="Experiment not found")
    return ExperimentResponse(
        id=experiment.id,
        name=experiment.name,
        hypothesis=experiment.hypothesis,
        description=experiment.description,
        status=experiment.status,
        created_at=experiment.created_at,
        variants=experiment.variants
    )


@router.put("/experiment/{experiment_id}", status_code=200)
async def update_experiment(experiment_id: UUID, update: ExperimentUpdate):
    experiment = repo.get_by_id(experiment_id)
    if not experiment:
        raise HTTPException(status_code=404, detail="Experiment not found")
    if update.status:
        experiment.status = update.status
    # For demo, ignore tags
    repo.update(experiment)


@router.delete("/experiment/{experiment_id}", status_code=204)
async def archive_experiment(experiment_id: UUID):
    experiment = repo.get_by_id(experiment_id)
    if not experiment:
        raise HTTPException(status_code=404, detail="Experiment not found")
    if experiment.status == ExperimentStatus.RUNNING:
        raise HTTPException(status_code=403, detail="Cannot archive a running experiment")
    experiment.status = ExperimentStatus.ARCHIVED
    repo.update(experiment)


@router.get("/experiment/{experiment_id}/user/{user_id}/variant", response_model=Variant)
async def get_experiment_variant(experiment_id: UUID, user_id: str) -> Variant:
    experiment = repo.get_by_id(experiment_id)
    if not experiment:
        raise HTTPException(status_code=404, detail="Experiment not found")
    variant = experiment.assign_variant(user_id)
    return variant


@router.post("/experiment/{experiment_id}/user/{user_id}/metric", status_code=204)
async def post_experiment_metric(experiment_id: UUID, user_id: str, metric: MetricValue):
    # For demo, we will assign variant here again to ensure 
    # we have the variant name for the metric. 
    # In a real implementation, you would likely want to store 
    # the assigned variant in a more persistent way 
    # (like a database) and retrieve it here instead of re-assigning.
    variant = await get_experiment_variant(experiment_id, user_id)

    metrics_repo.save(
        experiment_id=experiment_id,
        user_id=user_id,
        variant_name=variant.name,
        metric_key=metric.metric_key,
        metric_value=metric.value
    )


@router.get("/experiment/{experiment_id}/data")
async def get_experiment_data(experiment_id: UUID):
    return metrics_repo.get_by_id(experiment_id)