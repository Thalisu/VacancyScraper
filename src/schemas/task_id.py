from pydantic import BaseModel, Field


class TaskId(BaseModel):
    task_id: str = Field(max_length=36, min_length=36)
