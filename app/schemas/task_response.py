from typing import Union
from pydantic import BaseModel, Field

class TaskResponse(BaseModel):
    task_type: str = Field(description="Type of task")
    confidence: float = Field(ge=0, le=1)
    answer: Union[str, int, float]