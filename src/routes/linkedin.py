from fastapi import APIRouter, HTTPException
from src.scrapers.linkedin_scraper import LinkedinJobs

from src.schemas.linkedin import JobRequests
from src.models.responses import LinkedInJobResponses

from src.exceptions import MissingCookies, InvalidCookiesOrUrl

router = APIRouter()


@router.get("/linkedin")
async def search_job(request: JobRequests) -> LinkedInJobResponses:
    try:
        jobs = LinkedinJobs(request)
    except InvalidCookiesOrUrl:
        raise HTTPException(status_code=400, detail="Invalid cookies or url")
    except MissingCookies:
        raise HTTPException(status_code=400, detail="missing authentication")

    return await jobs.get()
