from pydantic import BaseModel


class Job(BaseModel):
    title: str
    url: str
    enterprise: str
    img: str
