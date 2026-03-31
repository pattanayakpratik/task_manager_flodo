from pydantic import BaseModel
from typing import Optional

class TaskBase(BaseModel):
    title: str
    description: str
    due_date: str
    status: str
    blocked_by_id: Optional[int] = None
    sort_order: int = -1

class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: int
    sort_order: int

    class Config:
        from_attributes = True

class TaskReorder(BaseModel):
    id: int
    sort_order: int