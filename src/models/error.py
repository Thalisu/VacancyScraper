from typing import TypedDict


class ErrorDetail(TypedDict):
    status_code: int
    message: str
