from db.session import get_db
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from services.auth import verify_jwt
from services.auth0 import verify_auth0_jwt
from sqlalchemy.ext.asyncio import AsyncSession

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security), db: AsyncSession = Depends(get_db)):
    try:
        return await verify_auth0_jwt(db, credentials)
    except HTTPException:
        return await verify_jwt(db, credentials)