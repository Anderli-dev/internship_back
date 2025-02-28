from db.schemas.UserSchema import UserSignIn
from db.session import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from services.auth import authenticate_user, create_access_token
from sqlalchemy.ext.asyncio import AsyncSession
from db.schemas.TokenSchema import Token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/token", response_model=Token)
async def login_for_access_token(user_data: UserSignIn, db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(user_data.email, user_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token = await create_access_token(data={"sub": user.username})
    
    return Token.model_validate({"access_token": access_token, "token_type": "bearer"})
