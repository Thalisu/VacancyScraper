from rq import Queue

from src.models.task import Task
from typing import Any

from .connection import redis_conn

queue = Queue(connection=redis_conn)


def enqueue(task: Any, *args: Any) -> dict[str, str]:
    job = queue.enqueue(task, *args)  # type: ignore
    return {"task_id": job.id}


def get_job(task_id: str) -> Task | None:
    task = queue.fetch_job(task_id)

    if not task:
        return None

    task_status = task.get_status(refresh=True)

    if not task_status:
        return None

    return {
        "task_result": task.result,
        "task_status": task_status,
    }


def get_queue_size() -> int:
    return queue.count


if __name__ == "__main__":
    queue.empty()
