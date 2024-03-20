from fastapi import FastAPI
from routers import user, task
from database import engine

app = FastAPI()

app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(task.router, prefix="/tasks", tags=["tasks"])
