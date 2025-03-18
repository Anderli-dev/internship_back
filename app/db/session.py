from core.logger import logger
from core.settings import settings
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(settings.database_url, echo=True, future=True)

AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

async def get_db() -> AsyncSession:
    try:
        async with AsyncSessionLocal() as session:
            yield session
            
    except SQLAlchemyError as e:
        logger.error(f"SQLAlchemyError: {str(e)}")
        raise HTTPException(status_code=500, detail="Database connection failed!")