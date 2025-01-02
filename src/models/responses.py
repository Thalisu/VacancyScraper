from typing import TypedDict, Optional
from .job import Data
from .error import ErrorDetail


class LinkedInJobResponse(TypedDict):
    response: Data
    error: Optional[ErrorDetail]
