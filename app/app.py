from fastapi import FastAPI, Request, Depends
from typing import Annotated
from app.routes import todo
from dotenv import load_dotenv
import os

app = FastAPI()
load_dotenv()

# include route
app.include_router(todo.router)

@app.get("/")
def root():  #Depends means we can insert values at run time like sql injection
    return {"message": "Hello Fastapi",
            "app_name": os.getenv("APP_NAME"),
            "app_env": os.getenv("APP_ENV")
    }