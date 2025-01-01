from fastapi import APIRouter, HTTPException
from src.models.task import Task
from src.schemas.task_id import TaskId
from src.scrapers.linkedin_scraper import LinkedinJobs
from src.redis.queue import enqueue, get_job, get_queue_size
from src.schemas.linkedin import JobRequests

router = APIRouter(prefix="/linkedin")


async def get_linkedin_jobs(request: JobRequests):
    return await LinkedinJobs(jobRequests=request).get()


@router.get("/")
async def search_job(request: JobRequests) -> dict[str, str]:
    task_id = enqueue(get_linkedin_jobs, request)

    return task_id


@router.get("/queue")
async def test_enqueue() -> dict[str, int]:
    return {"queue_size": get_queue_size()}


@router.get("/get")
async def get_task(request: TaskId) -> Task:
    task = get_job(request.task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task
