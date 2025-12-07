# app/jwt_utils.py
import jwt
from datetime import datetime, timedelta
from app.config import settings

def create_access_token(data: dict):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(seconds=settings.ACCESS_EXPIRES)
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

def create_refresh_token(data: dict):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(seconds=settings.REFRESH_EXPIRES)
    return jwt.encode(payload, settings.REFRESH_SECRET_KEY, algorithm="HS256")

def decode_access(token: str):
    return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

def decode_refresh(token: str):
    return jwt.decode(token, settings.REFRESH_SECRET_KEY, algorithms=["HS256"])
