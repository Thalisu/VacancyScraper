from fastapi import APIRouter

from src.routes.linkedin import router as linkedin_router

router = APIRouter()

router.include_router(linkedin_router)
