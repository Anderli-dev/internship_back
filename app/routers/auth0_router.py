from urllib.parse import quote

from services.auth_service import Auth0Service
from core.logger import logger
from core.settings import settings
from db.models.user import User
from db.session import get_db
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

router = APIRouter(prefix="/auth0", tags=["Auth0"])

@router.get("/token")
async def login_for_access_token_Auth0():
    # This function redirects to callback with code
    logger.info("Auth0 token Login.")
    auth_url = (
        f"https://{settings.auth0_domain}/authorize"
        f"?response_type=code"
        f"&client_id={settings.client_id}"
        f"&redirect_uri=http://{settings.auth0_app_host}:{settings.app_port}/auth0/callback"
        f"&audience={settings.auth0_audience}"
    )
    return RedirectResponse(auth_url)

@router.get("/callback")
async def callback(request: Request, db: AsyncSession = Depends(get_db)) -> dict:
    # Callback getting code for getting token from Auth0
    logger.info("Callback for Auth0 token.")
    auth_service = Auth0Service(db)
    code = request.query_params.get("code")
    
    if not code:
        logger.error("Missing code for Auth0 token.")
        raise HTTPException(status_code=400, detail="Missing code parameter!")

    tokens = auth_service.get_tokens(code)
    
    email = auth_service.get_email_from_token(tokens["access_token"])
    
    # Creating user if it dose not exist
    existing_user = await db.execute(select(User).filter(User.email == email))
    existing_user = existing_user.scalars().first()
    
    if not existing_user:
        logger.info("Auth0 user dose not exist.")
        db_user = User(email=email)
        logger.debug("Adding user to db")
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        logger.info("Auth0 user created.")
    
    logger.info("Auth0 token Login success!")
    return {"access_token": tokens["access_token"], "email": email}

@router.get("/logout")
async def logout():
    logger.info("Auth0 Logout")
    return_to = quote(f"http://{settings.auth0_app_host}:{settings.app_port}/docs", safe='')
    logout_url = f"https://{settings.auth0_domain}/v2/logout?client_id={settings.client_id}&returnTo={return_to}"
    return RedirectResponse(logout_url)