from typing import TypedDict, List, Optional
from .error import ErrorDetail


class Job(TypedDict):
    title: str
    url: str
    enterprise: str
    img: str
    state: str
    location: str


Jobs = List[Job]


class Data(TypedDict):
    keywords: str
    error: Optional[ErrorDetail]
    jobs: Jobs
