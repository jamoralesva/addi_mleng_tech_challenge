from fastapi import APIRouter

from .endpoints.experiments import router as experiments_router

router = APIRouter()
router.include_router(experiments_router)