from core.logger import logger
from db.schemas.TokenSchema import Token
from db.schemas.UserSchema import UserSignIn
from db.session import get_db
from fastapi import APIRouter, Depends
from services.auth_service import AuthService
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/token", response_model=Token)
async def login_for_access_token(user_data: UserSignIn, db: AsyncSession = Depends(get_db)) -> dict:
    logger.info("Own token Login.")
    
    service = AuthService(db)
    token = await service.login_for_access_token(user_data)
    
    logger.info("Own token Login success!")
    
    return token
