# app/redis_utils.py
import redis
from app.config import settings

redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)

def blacklist_token(token: str):
    redis_client.set(token, "blacklisted")

def is_token_blacklisted(token: str):
    return redis_client.exists(token) == 1
