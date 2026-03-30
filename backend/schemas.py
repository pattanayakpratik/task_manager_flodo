from pydantic import BaseModel
from typing import Optional

class TaskBase(BaseModel):
    title: str
    description: str
    due_date: str
    status: str
    blocked_by_id: Optional[int] = None

class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: int

    class Config:
        orm_mode = True