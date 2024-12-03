from fastapi import APIRouter

from src.scrapers.linkedin_scraper import LinkedinJobs

from src.exceptions import MissingKeywords
from fastapi import HTTPException

from src.models.job import Job
from src.schemas.linkedin import JobRequest

router = APIRouter()


@router.get("/linkedin")
def search_job(request: JobRequest) -> Job:
    try:
        jobs = LinkedinJobs(
            keywords=request.keywords,
            location=request.location,
            timeframe=request.timeframe,
            remote=request.remote,
        )
    except MissingKeywords:
        raise HTTPException(status_code=400, detail="Keywords are required")

    return jobs.get(page=request.page)
