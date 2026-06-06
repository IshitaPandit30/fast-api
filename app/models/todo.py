from typing import Optional 
from pydantic import BaseModel

class CreateTodo(BaseModel):
   content:str
   is_completed: bool =False