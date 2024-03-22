from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Task, User
from auth import get_user_id_from_token

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(get_user_id_from_token), db: Session = Depends(get_db)
):
    user_id = token
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user


@router.get("/")
def get_tasks(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tasks = db.query(Task).filter(Task.user_id == user.id).all()
    return [
        {
            "id": task.id,
            "task_description": task.task_description,
            "is_done": task.is_done,
        }
        for task in tasks
    ]


@router.post("/")
def create_task(
    task_description: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    new_task = Task(user_id=user.id, task_description=task_description)
    db.add(new_task)
    db.commit()
    return {"message": "Task created successfully", "task_id": new_task.id}


@router.delete("/{task_id}")
def delete_task(
    task_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}


@router.put("/{task_id}")
def update_task(
    task_id: int,
    task_description: str,
    is_done: bool = None,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.task_description = task_description
    if is_done is not None:
        task.is_done = is_done
    db.commit()
    return {"message": "Task updated successfully"}
