from fastapi import APIRouter, Depends
from app.models.todo import CreateTodo
from typing import Annotated
from app.DB.db import get_db
from sqlalchemy.orm import Session
from app.DB.schema.todo_schema import TodoSchema
from sqlalchemy import select
from app.dependencies import authenticate_user

router = APIRouter(prefix="/api", dependencies=[Depends(authenticate_user)])

@router.get("/todos")
def index(db:Annotated[Session, Depends(get_db)]):
    todos=db.query(TodoSchema).all()
    return {"message": "List of todos", "items": todos}

@router.post("/todos")
def store(item:CreateTodo, db: Annotated[Session, Depends(get_db)]):
    todo = TodoSchema(content=item.content, is_completed=item.is_completed)
    # add to db and commit 
    db.add(todo)
    db.commit()
    # to get refresh data
    db.refresh(todo)
    return {"message": "Todo created", "todo": todo}

@router.get("/todos/individual")
def show(db:Annotated[Session, Depends(get_db)]):
    stmt= select(TodoSchema.id, TodoSchema.content)
    result = db.execute(stmt).mappings().all() #the default return is tupple so it won't parse, that's why we require mappings
    print(f"Specific Todos: {result}")

    return {"message": "Specific Todos", "todos": result}

@router.get("/todos/{id}")
def show(id:int, db:Annotated[Session, Depends(get_db)]):
    item =  db.query(TodoSchema).filter(TodoSchema.id == id).first()

    return item

@router.delete("/todos/{id}")
def delete(id:int, db: Annotated[Session, Depends(get_db)]):
    todo= db.query(TodoSchema).filter(TodoSchema.id ==id).first()

    if not todo:
        return {"message": "Todo not found"}
    
    db.delete(todo)
    db.commit()

    return {"message": "Todo deleted"}

@router.put("/todos/{id}")
def update(id:int, item:CreateTodo, db:Annotated[Session, Depends(get_db)]):
    todo = db.query(TodoSchema).filter(TodoSchema.id ==id).first()

    if not todo:
        return {"message": "Todo not found"}

    todo.content = item.content
    todo.is_completed = item.is_completed

    db.commit()
    db.refresh(todo)
    return {"message": "Todo updated", "todo": todo}
