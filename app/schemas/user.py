# app/schemas/user.py
from pydantic import BaseModel

class UpdateUser(BaseModel):
    email: str | None = None
    password: str | None = None
