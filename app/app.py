from fastapi import FastAPI, Request, Depends
from typing import Annotated
from app.routes import todo, auth
from dotenv import load_dotenv
import os
from app.config.app_config import getAppConfig

# Import ALL models before create_all()
from app.DB.schema.todo_schema import TodoSchema
from app.DB.db import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)
load_dotenv()

# include route
app.include_router(todo.router)
app.include_router(auth.router)

@app.get("/")
def root():  #Depends means we can insert values at run time like sql injection
    config = getAppConfig()
    return {"message": "Hello Fastapi",
            "app_name": config.app_name,
            "app_env": config.app_env,
            "database_url": config.database_url
    }