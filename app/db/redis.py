from fastapi import HTTPException
import core.settings as settings
import redis.asyncio as aioredis
from core.settings import logger

REDIS_URL = settings.REDIS_URL

async def get_redis_connection() -> aioredis:
    try:
        redis = await aioredis.from_url(REDIS_URL, decode_responses=True)
        return redis
    except aioredis.RedisError as e:
        logger.error(f"Redis conection error:{str(e)}")
        raise HTTPException(status_code=500, detail="Redis connection failed!")