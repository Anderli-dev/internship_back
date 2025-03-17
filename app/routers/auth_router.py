from urllib.parse import quote

from core.settings import settings
from core.logger import logger
from db.models.user import User
from db.schemas.TokenSchema import Token
from db.schemas.UserSchema import UserSignIn
from db.session import get_db
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from services.auth import authenticate_user, create_access_token
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from utils.auth0.get_email_from_token import get_email_from_token
from utils.auth0.get_tokens import get_tokens

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/token", response_model=Token)
async def login_for_access_token(user_data: UserSignIn, db: AsyncSession = Depends(get_db)) -> dict:
    logger.info("Own token Login.")
    user = await authenticate_user(user_data.email, user_data.password, db)
    
    if not user:
        logger.error("User incorrect username or password!")
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token = await create_access_token(data={"user_email": user.email})
    logger.info("Own token Login success!")
    return {"access_token": access_token, "token_type": "bearer"}
