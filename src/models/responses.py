from typing import TypedDict, List, Optional
from .job import Jobs
from .error import ErrorDetail


class LinkedInJobResponse(TypedDict):
    keywords: str
    error: Optional[ErrorDetail]
    jobs: Jobs


LinkedInJobResponses = List[LinkedInJobResponse]
