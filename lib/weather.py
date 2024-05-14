import python_weather
import asyncio
import httpx
from fastapi import FastAPI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Change the token for every user
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0IiwiZXhwIjoxNzE1NzAzNzQyfQ.9I7SmovQpdNkl2ybLWjZJFkxK3tT9NyWAgvVO0MCyJ4"

app = FastAPI()


@app.get("/tasks")
async def req_tasks():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://127.0.0.1:8000/tasks/?token={TOKEN}")
        return response.json()


@app.post("/task")
async def post_task(desc: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"http://127.0.0.1:8000/tasks/?task_description={desc}&token={TOKEN}"
        )
        return response.json()


def get_tasks():
    tasks = asyncio.run(req_tasks())
    return tasks


def create_task(desc: str):
    task_response = asyncio.run(post_task(desc))
    return task_response
