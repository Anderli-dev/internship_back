from urllib.parse import quote

from core.settings import AUTH0_AUDIENCE, AUTH0_DOMAIN, CLIENT_ID, logger
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
async def login_for_access_token(user_data: UserSignIn, db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(user_data.email, user_data.password, db)
    if not user:
        logger.error("User incorrect username or password")
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token = await create_access_token(data={"user_email": user.email})
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/token/auth0")
async def login_for_access_token_Auth0():
    auth_url = (
        f"https://{AUTH0_DOMAIN}/authorize"
        f"?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri=http://localhost:8000/auth/callback"
        f"&audience={AUTH0_AUDIENCE}"
    )
    return RedirectResponse(auth_url)

@router.get("/callback")
async def callback(request: Request, db: AsyncSession = Depends(get_db)):
    code = request.query_params.get("code")
    
    if not code:
        raise HTTPException(status_code=400, detail="Missing code parameter!")

    tokens = await get_tokens(code)
    
    email = await get_email_from_token(tokens["access_token"])
    
    existing_user = await db.execute(select(User).filter(User.email == email))
    existing_user = existing_user.scalars().first()
    
    if not existing_user:
        db_user = User(email=email)
        logger.debug("Adding user to db")
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
    
    return {"access_token": tokens["access_token"], "email": email}

@router.get("/logout/auth0")
def logout():
    return_to = quote("http://localhost:8000/docs", safe='')
    logout_url = f"https://{AUTH0_DOMAIN}/v2/logout?client_id={CLIENT_ID}&returnTo={return_to}"
    return RedirectResponse(logout_url)
