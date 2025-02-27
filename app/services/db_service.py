from fastapi import HTTPException
from core.settings import logger
from db.redis import get_redis_connection
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

async def redis_test() -> str:
    logger.debug("Redis test.")
    
    redis = await get_redis_connection()
    await redis.set("test_key", "Hello, Redis!")
    value = await redis.get("test_key")
    
    return value

async def test_db_connection(db: AsyncSession) -> dict:
    logger.debug("PostgreSQL test.")
    
    try:
        result = await db.execute(text("SELECT 1"))
    except SQLAlchemyError as e:
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(status_code=500, detail="Database connection failed!")
    except Exception as e:
        logger.error(f"Unexpected error in test_db_connection: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error!")
    
    return {"db_status": "Connected", "result": result.scalar()}

    