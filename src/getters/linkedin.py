from src.exceptions import MissingKeywords, InvalidCookiesOrUrl, MissingCookies
from src.scrapers.linkedin_scraper import LinkedinJobs
from src.schemas.linkedin import JobRequest, JobResponse

import asyncio


async def get_jobs(jobRequest: JobRequest) -> JobResponse:
    base_response = {
        "keywords": jobRequest.keywords,
        "jobs": [],
        "error": None,
    }
    print(jobRequest)

    try:
        jobs = LinkedinJobs(
            keywords=jobRequest.keywords,
            location=jobRequest.location,
            timeframe=jobRequest.timeframe,
            remote=jobRequest.remote,
        )

    except MissingKeywords:
        return JobResponse.parse_obj(
            {
                **base_response,
                "error": {
                    "status_code": 400,
                    "message": "Keywords are required",
                },
            }
        )

    except InvalidCookiesOrUrl:
        return JobResponse.parse_obj(
            {
                **base_response,
                "error": {
                    "status_code": 400,
                    "message": "Invalid cookies or url",
                },
            }
        )
    except MissingCookies:
        return JobResponse.parse_obj(
            {
                **base_response,
                "error": {
                    "status_code": 400,
                    "message": "missing authentication",
                },
            }
        )

    base_response["jobs"] = await asyncio.to_thread(
        jobs.get, page=jobRequest.page
    )

    return JobResponse.parse_obj(base_response)
