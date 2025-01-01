from typing import TypedDict, Optional, Any, Union, List, Dict
from rq.job import JobStatus


class Task(TypedDict):
    task_result: Optional[Union[List[Dict[str, Any]], Dict[str, Any]]]
    task_status: JobStatus
