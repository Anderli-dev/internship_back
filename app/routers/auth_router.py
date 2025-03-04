from fastapi.responses import RedirectResponse
from core.settings import AUTH0_AUDIENCE, AUTH0_DOMAIN, logger, CLIENT_ID, CLIENT_SECRET
from db.schemas.TokenSchema import Token
from db.schemas.UserSchema import UserSignIn
from db.session import get_db
from fastapi import APIRouter, Depends, HTTPException, Request
from services.auth import authenticate_user, create_access_token
from sqlalchemy.ext.asyncio import AsyncSession
import requests

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
        f"&scope=openid profile email"
        f"&audience={AUTH0_AUDIENCE}"
    )
    return RedirectResponse(auth_url)

@router.get("/callback")
async def callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Missing code parameter")

    token_data = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "redirect_uri": "http://localhost:8000/auth/callback"
    }

    response = requests.post(f"https://{AUTH0_DOMAIN}/oauth/token", json=token_data)
    
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to fetch token")

    tokens = response.json()
    return {"access_token": tokens["access_token"], "id_token": tokens["id_token"]}

@router.get("/logout/auth0")
def logout():
    logout_url = f"https://{AUTH0_DOMAIN}/v2/logout?returnTo=http://localhost:8000"
    return RedirectResponse(logout_url)
