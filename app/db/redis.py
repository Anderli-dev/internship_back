import redis.asyncio as aioredis
from core.settings import settings


async def get_redis_connection() -> aioredis:
    redis = await aioredis.from_url(settings.redis_url, decode_responses=True)
    
    return redis
