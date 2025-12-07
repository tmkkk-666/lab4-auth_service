# app/routers/user_router.py
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from app.jwt_utils import decode_access
from app.redis_utils import is_token_blacklisted
from app.database import SessionLocal
from app.models.user import User
from app.schemas.user import UpdateUser

router = APIRouter(prefix="/user")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)):
    if not authorization:
        raise HTTPException(401, "Missing token")

    token = authorization.split(" ")[1]
    if is_token_blacklisted(token):
        raise HTTPException(401, "Token is blacklisted")

    payload = decode_access(token)
    user = db.query(User).filter_by(id=payload["sub"]).first()
    if not user:
        raise HTTPException(401, "User not found")

    return user


@router.put("/update")
def update_user(data: UpdateUser, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if data.email:
        user.email = data.email
    if data.password:
        user.hashed_password = bcrypt.hash(data.password)

    db.commit()
    return {"message": "Updated"}


@router.get("/history")
def history(user: User = Depends(get_current_user)):
    return [
        {"user_agent": h.user_agent, "timestamp": h.timestamp}
        for h in user.login_history
    ]
