import core.settings as settings
import redis.asyncio as aioredis
from core.settings import logger

REDIS_URL = settings.REDIS_URL

async def get_redis_connection() -> aioredis:
    try:
        redis = await aioredis.from_url(REDIS_URL, decode_responses=True)
        return redis
    except Exception as e:
        logger.error(f"Redis conection error:{str(e)}")