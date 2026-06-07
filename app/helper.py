from pwdlib import PasswordHash
from argon2 import PasswordHasher
import jwt
from app.config.app_config import getAppConfig
from datetime import datetime, timezone, timedelta

ph = PasswordHasher()

def hashPassword(password: str) -> str:
    return ph.hash(password)

def verifyPassword(password: str, hashed_password: str) -> bool:
    try:
        return ph.verify(hashed_password, password)
    except Exception:
        return False

def createAccessToken(data:dict, expire_minutes:int):
    config = getAppConfig()
    to_encode = data.copy()
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)
    to_encode.update({"exp": expires_at})
    encoded_jwt =jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt

def decodeAccessToken(token:str):
    config = getAppConfig()
    payload= jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
    return payload