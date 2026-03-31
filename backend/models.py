from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    due_date = Column(String, nullable=False) # Storing as ISO 8601 string for simplicity
    status = Column(String, default="To-Do", nullable=False) 
    blocked_by_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    sort_order = Column(Integer, default=-1)