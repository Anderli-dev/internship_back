import redis.asyncio as aioredis
import core.settings as settings

REDIS_URL = settings.REDIS_URL

async def get_redis_connection() -> aioredis:
    redis = await aioredis.from_url(REDIS_URL, decode_responses=True)
    return redis
