from fastapi import APIRouter
from models import User

router = APIRouter()

@router.post("/users/")
def create_user(username: str):
    # Create a new user
    pass