from core.settings import settings
import uvicorn

from db.redis import get_redis_connection
from db.session import get_db

from fastapi import Depends, FastAPI

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from utils.cors import add_cors_middleware

app = FastAPI()

add_cors_middleware(app)

@app.get("/")
async def home() -> dict:
    return {"status_code": 200, "detail": "ok", "result": "working"}

@app.get("/redis_test")
async def redis_test() -> dict:
    redis = await get_redis_connection()
    await redis.set("test_key", "Hello, Redis!")
    value = await redis.get("test_key")
    return {"redis_value": value}

@app.get("/db_test")
async def test_db_connection(db: AsyncSession = Depends(get_db)) -> dict:
    try:
        result = await db.execute(text("SELECT 1"))
        return {"db_status": "Connected", "result": result.scalar()}
    except Exception as e:
        return {"db_status": "Error", "details": str(e)}
    
if __name__ == "__main__":
    # To make the work more comfortable, you can run a script. 
    # It is better to do this in a separate file like run.py.
    uvicorn.run("main:app", host=settings.app_host, port=settings.app_port, reload=True)
    