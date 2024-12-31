from fastapi import APIRouter

from src.routes.healthcheck import router as healthcheck_router
from src.routes.linkedin import router as linkedin_router

router = APIRouter()

router.include_router(healthcheck_router)
router.include_router(linkedin_router)
