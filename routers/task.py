from fastapi import APIRouter
from models import Task

router = APIRouter()

@router.get("/tasks/{user_id}")
def get_tasks(user_id: int):
    # Retrieve tasks associated with the user_id
    pass

@router.post("/tasks/{user_id}")
def create_task(user_id: int, task_description: str):
    # Create a new task associated with the user_id
    pass

@router.delete("/tasks/{user_id}/{task_id}")
def delete_task(user_id: int, task_id: int):
    # Delete the task with the given task_id for the user_id
    pass