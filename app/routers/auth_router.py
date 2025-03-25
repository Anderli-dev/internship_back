from core.logger import logger
from db.schemas.token_schema import Token
from db.schemas.user_schema import UserSignIn
from db.session import get_db
from fastapi import APIRouter, Depends, HTTPException
from services.auth import authenticate_user, create_access_token
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/token", response_model=Token)
async def login_for_access_token(user_data: UserSignIn, db: AsyncSession = Depends(get_db)) -> dict:
    logger.info("Own token Login.")
    user = await authenticate_user(user_data.email, user_data.password, db)
    
    if not user:
        logger.error("User incorrect username or password!")
        raise HTTPException(status_code=401, detail="Incorrect username or password")
        
    access_token = await create_access_token(data={"user_email": user.email})
    logger.info("Own token Login success!")
    return {"access_token": access_token, "token_type": "bearer"}
