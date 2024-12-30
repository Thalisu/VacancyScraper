from typing import TypedDict, List, Optional
from .job import Jobs
from .error import Error


class LinkedInJobResponse(TypedDict):
    keywords: str
    error: Optional[Error]
    jobs: Jobs


LinkedInJobResponses = List[LinkedInJobResponse]
