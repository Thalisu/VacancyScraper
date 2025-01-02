from typing import TypedDict, Optional, Union, Dict, Any
from .responses import LinkedInJobResponse
from rq.job import JobStatus


class Task(TypedDict):
    task_result: Optional[Union[LinkedInJobResponse, Dict[str, Any]]]
    task_status: JobStatus
