import os
from typing import Any


def get_config(name: str) -> Any | None:
    return os.environ.get(name)
