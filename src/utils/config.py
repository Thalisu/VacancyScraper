import os


def get_config(name: str) -> str | None:
    return os.environ.get(name)
