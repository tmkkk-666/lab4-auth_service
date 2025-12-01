# app/models/user.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    login_history = relationship("LoginHistory", back_populates="user")


class LoginHistory(Base):
    __tablename__ = "login_history"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user_agent = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="login_history")
