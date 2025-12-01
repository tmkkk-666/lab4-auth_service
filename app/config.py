# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    REFRESH_SECRET_KEY: str
    ACCESS_EXPIRES: int = 900
    REFRESH_EXPIRES: int = 60 * 60 * 24 * 30
    REDIS_URL: str

    class Config:
        env_file = ".env"

settings = Settings()