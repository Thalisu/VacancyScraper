from typing import TypedDict, List


class Job(TypedDict):
    title: str
    url: str
    enterprise: str
    img: str


Jobs = List[Job]
