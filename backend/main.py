from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import asyncio
from typing import List

import models, schemas
from database import engine, get_db

# create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Management API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

@app.get("/tasks/", response_model=List[schemas.TaskResponse])
def read_tasks(db: Session = Depends(get_db)):
    return db.query(models.Task).order_by(models.Task.sort_order).all()

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
    
    # Capture the sort_order of the task being deleted
    deleted_order = db_task.sort_order

    # Delete the task
    db.delete(db_task)
    
    # Shift all subsequent tasks up by one if the deleted task had a valid priority
    if deleted_order != -1:
        db.query(models.Task).filter(models.Task.sort_order > deleted_order).update(
            {models.Task.sort_order: models.Task.sort_order - 1}
        )
        
    db.commit()
    return {"message": "Task deleted and priority list updated"}

@app.post("/tasks/reorder")
async def reorder_tasks(updates: List[schemas.TaskReorder], db: Session = Depends(get_db)):
    await asyncio.sleep(2)
    # Fetch all tasks in one query for efficiency
    task_map = {
        task.id: task
        for task in db.query(models.Task).filter(models.Task.id.in_([u.id for u in updates])).all()
    }

    # Update the sort order
    for update in updates:
        if update.id in task_map:
            task_map[update.id].sort_order = update.sort_order
            
    db.commit()
    return {"message": "Tasks reordered successfully"}