from typing import TypedDict
from pydantic import BaseModel


class ErrorDetail(TypedDict):
    status_code: int
    message: str


class Error(BaseModel):
    error: ErrorDetail
