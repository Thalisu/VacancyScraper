import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from src.models.error import ErrorDetail
from src.models.responses import LinkedInJobResponse
from src.scrapers.linkedin_scraper import LinkedinJobs
from src.redis.queue import enqueue, get_job, get_queue_size
from src.schemas.linkedin import JobRequests

router = APIRouter(prefix="/linkedin")


async def get_linkedin_jobs(request: JobRequests) -> LinkedInJobResponse:
    try:
        response = await LinkedinJobs(jobRequests=request).get()
        data = LinkedInJobResponse(response=response, error=None)
    except Exception as e:
        data = LinkedInJobResponse(
            response=None, error=ErrorDetail(status_code=500, message=str(e))
        )

    return data


@router.post("/")
async def search_job(request: JobRequests) -> dict[str, str]:
    task_id = enqueue(get_linkedin_jobs, request)

    return task_id


@router.get("/queue")
async def test_enqueue() -> dict[str, int]:
    return {"queue_size": get_queue_size()}


@router.websocket("/ws/{task_id}")
async def get_task(websocket: WebSocket, task_id: str) -> None:
    await websocket.accept()
    try:
        while True:
            task = get_job(task_id)
            if not task:
                await websocket.send_json(
                    {"status": "error", "detail": "Task not found"}
                )
                await websocket.close()
                return None

            if task["task_status"] == "failed":
                await websocket.send_json(task)
                await websocket.close()
                return None

            if task["task_result"]:
                break

            await websocket.send_json(task)

            await asyncio.sleep(0.2 if task["task_status"] == "started" else 1)

        await websocket.send_json(task)
        await websocket.close()
    except WebSocketDisconnect:
        pass
    except Exception as e:
        await websocket.send_json(
            {
                "task_result": LinkedInJobResponse(
                    response=None,
                    error=ErrorDetail(status_code=500, message=str(e)),
                ),
                "task_status": "failed",
            }
        )
        await websocket.close()
