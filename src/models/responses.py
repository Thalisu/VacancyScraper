from typing import List, TypedDict, Optional
from .job import Data
from .error import ErrorDetail


class LinkedInJobResponse(TypedDict):
    response: Optional[List[Data]]
    error: Optional[ErrorDetail]
