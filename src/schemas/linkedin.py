from pydantic import BaseModel, Field

from src.models.job import Job
from src.models.error import Error

from typing import List, Optional


class JobRequest(BaseModel):
    keywords: str = Field(min_length=3, max_length=255)
    location: str = Field(default="Brazil", max_length=32)
    timeframe: str = Field(default="r86400", max_length=16)
    remote: str = Field(default="1%2C2%2C3", max_length=9)
    page: int = Field(default=0)


JobRequests = List[JobRequest]
