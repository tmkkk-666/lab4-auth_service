# app/routers/auth_router.py
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from app.database import SessionLocal
from app.models.user import User, LoginHistory
from app.schemas.auth import RegisterRequest, LoginRequest, RefreshRequest
from app.jwt_utils import create_access_token, create_refresh_token, decode_refresh
from app.redis_utils import blacklist_token

router = APIRouter(prefix="/auth")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(User).filter_by(email=data.email).first():
        raise HTTPException(400, "Email already registered")

    user = User(email=data.email, hashed_password=bcrypt.hash(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User registered"}


@router.post("/login")
def login(data: LoginRequest, request: Request, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=data.email).first()
    if not user or not bcrypt.verify(data.password, user.hashed_password):
        raise HTTPException(401, "Invalid credentials")

    # save login history
    history = LoginHistory(
        user_id=user.id,
        user_agent=request.headers.get("User-Agent")
    )
    db.add(history)
    db.commit()

    return {
        "access_token": create_access_token({"sub": user.id}),
        "refresh_token": create_refresh_token({"sub": user.id})
    }


@router.post("/refresh")
def refresh(data: RefreshRequest):
    payload = decode_refresh(data.refresh_token)
    uid = payload["sub"]
    return {"access_token": create_access_token({"sub": uid})}


@router.post("/logout")
def logout(data: RefreshRequest):
    blacklist_token(data.refresh_token)
    return {"message": "Logged out"}
