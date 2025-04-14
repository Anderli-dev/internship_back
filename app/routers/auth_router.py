
from core.logger import logger
from db.schemas.TokenSchema import Token
from db.schemas.UserSchema import UserSignIn
from db.session import get_db
from fastapi import APIRouter, Depends, HTTPException
from services.auth_service import AuthService
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/token", response_model=Token)
async def login_for_access_token(user_data: UserSignIn, db: AsyncSession = Depends(get_db)) -> dict:
    logger.info("Own token Login.")
    service = AuthService(db)
    user = await service.authenticate_user(user_data.email, user_data.password)
    
    if not user:
        logger.error("Incorrect username or password!")
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token = await service.create_access_token(data={"user_email": user.email})
    logger.info("Own token Login success!")
    return {"access_token": access_token, "token_type": "bearer"}
