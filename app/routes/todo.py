from fastapi import APIRouter
from app.models.todo import CreateTodo

router = APIRouter()

@router.get("/todos")
def index():
    return {"message": "List of todos"}

@router.post("/todos")
def store(item:CreateTodo):
    return {"message": "Todo created", "todo": item}