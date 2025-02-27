from db.session import get_db
from fastapi import APIRouter, Depends, HTTPException
from services import db_service
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/db_tests", tags=["tests"])


@router.get("/redis", response_model=dict[str, str])
async def redis_test():
    test_response = await db_service.redis_test()
    
    if test_response is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve value from Redis!")
    return {"redis_test_response": test_response}
    
@router.get("/psql", response_model=dict[str, str | int])
async def test_db_connection(db: AsyncSession = Depends(get_db)):
    db_response = await db_service.test_db_connection(db)
    
    if db_response is None:
            raise HTTPException(status_code=500, detail="Database query returned no result!")
    return db_response