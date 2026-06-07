from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from app.models.auth import Register
from app.DB.schema import CreateUserSchema
from app.DB.db import get_db
from sqlalchemy.orm import Session
from typing import Annotated
from app.helper import hashPassword, verifyPassword, createAccessToken

router =APIRouter(prefix="/auth")

@router.post("/register")
def register(data: Register, db: Annotated[Session, Depends(get_db)]):
    existing_user = db.query(CreateUserSchema).filter(CreateUserSchema.email == data.email).first()
    if existing_user:
        return JSONResponse(status_code=400, content={"message": "Email already exists"})

    hashed_password = hashPassword(data.password)
    new_user = CreateUserSchema(name=data.name, email=data.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User created successfully",
        "user": {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email
        }
    }

@router.post("/login")
def login(data:Register, db: Annotated[Session, Depends(get_db)]):
    user = db.query(CreateUserSchema).filter(CreateUserSchema.email == data.email).first()
    if not user:
        return JSONResponse(status_code=400, content={"message": "Invalid email or password"})

    if not verifyPassword(data.password, user.password):
        return JSONResponse(status_code=400, content={"message": "Invalid email or password"})
    
    payload ={
        "id": user.id,
        "name": user.name,
        "email": user.email
    }

    token = createAccessToken(payload, expire_minutes=30)
    payload["access_token"] = "Bearer " +  token

    return {
        "message": "Login successful",
        "data": payload
    }
