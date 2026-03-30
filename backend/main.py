from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import asyncio
from typing import List

import models, schemas
from database import engine, get_db

# create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Management API")

@app.get("/tasks/", response_model=List[schemas.TaskResponse])
def read_tasks(db: Session = Depends(get_db)):
    return db.query(models.Task).all()

@app.post("/tasks/", response_model=schemas.TaskResponse)
async def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    await asyncio.sleep(2)
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.put("/tasks/{task_id}", response_model=schemas.TaskResponse)
async def update_task(task_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db)):
    await asyncio.sleep(2)
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task.dict().items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return {"message": "Task deleted successfully"}