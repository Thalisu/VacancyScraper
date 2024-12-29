from fastapi import APIRouter
from src.getters.linkedin import get_jobs

from src.schemas.linkedin import JobRequest, JobResponse
from typing import List

import asyncio

router = APIRouter()


@router.get("/linkedin")
async def search_job(request: List[JobRequest]) -> List[JobResponse]:
    job_cards = [get_jobs(jobRequest) for jobRequest in request]

    return await asyncio.gather(*job_cards)
