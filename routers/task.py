from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Task, User

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{user_id}")
def get_tasks(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    tasks = db.query(Task).filter(Task.user_id == user_id).all()
    return [{"id": task.id, "task_description": task.task_description, "is_done": task.is_done} for task in tasks]

@router.post("/{user_id}")
def create_task(user_id: int, task_description: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    new_task = Task(user_id=user_id, task_description=task_description)
    db.add(new_task)
    db.commit()
    return {"message": "Task created successfully"}

@router.delete("/{user_id}/{task_id}")
def delete_task(user_id: int, task_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}

@router.put("/{user_id}/{task_id}")
def update_task(user_id: int, task_id: int, task_description: str, is_done: bool = None, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.task_description = task_description
    if is_done is not None:
        task.is_done = is_done
    db.commit()
    return {"message": "Task updated successfully"}