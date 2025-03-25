import requests
from core.logger import logger
from core.settings import settings
from db.models import User
from fastapi import HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from utils.auth0.get_management_token import get_management_token
from utils.decorators.user_action_error_check import user_action_error_check


class UserDeleteService:
    @user_action_error_check(secur=True)
    async def delete_user(self, db: AsyncSession, payload: dict, user: User):
        if "sub" in payload:
            await self.delete_auth0_user(payload)
            
        return await self.delete_user_from_db(db, user)
    
    @staticmethod
    async def delete_user_from_db(db: AsyncSession, user: User):
        logger.debug("Deleting user in db")
        await db.delete(user)
        await db.commit()

        return {"message": "User deleted successfully"}
    
    @staticmethod
    async def delete_auth0_user(payload: dict):
        token = await get_management_token()

        url = f'https://{settings.auth0_domain}/api/v2/users/{payload["sub"]}'
        headers = {'Authorization': f'Bearer {token}'}

        response: Response = requests.delete(url, headers=headers)
        
        if response.status_code != 204:
            logger.error(f"Auth0 delete failed: {response.content}")
            detail = response.json().get("message", "Error deleting user from authentication provider.")
            raise HTTPException(status_code=response.status_code, detail=detail)