from fastapi import HTTPException
from core.logger import logger
import redis.asyncio as aioredis
from core.settings import settings


async def get_redis_connection() -> aioredis:
    try:
        redis = await aioredis.from_url(settings.redis_url, decode_responses=True)
        return redis
    except aioredis.RedisError as e:
        logger.error(f"Redis conection error:{str(e)}")
        raise HTTPException(status_code=500, detail="Redis connection failed!")
