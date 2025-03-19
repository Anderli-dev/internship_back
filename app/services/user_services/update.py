import requests
from core.logger import logger
from core.settings import settings
from db.models import User
from db.schemas.UserSchema import UserUpdate
from fastapi import HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from utils.auth0.get_management_token import get_management_token
from utils.decorators.user_action_error_check import user_action_error_check
from utils.hash_password import hash_password


class UserUpdateService:
    @user_action_error_check(optional_user=True)
    async def update_user(self, user_id: int, payload: dict, db: AsyncSession, user_data: UserUpdate, user: User):
        if "sub" in payload:
            await self.update_auth0_user(payload, user_data)
            
        return await self.update_user_from_db(db, user, user_data)
    
    async def update_user_from_db(self, db: AsyncSession, user: User, user_data: UserUpdate):
        logger.debug("Setting up user data")
        # Updating not None fields
        for key, data in user_data.model_dump(exclude_unset=True).items():
            if key == "password":
                data = hash_password(data)
            setattr(user, key, data)
        
        logger.debug("Saving new user data in db")
        
        await db.commit()
        await db.refresh(user)
        
        logger.info("Updating user successful.")
        return user
    
    async def update_auth0_user(self, payload: dict, user_data: UserUpdate):
        token = await get_management_token()
        
        url = f'https://{settings.auth0_domain}/api/v2/users/{payload["sub"]}'
        headers = {'Authorization': f'Bearer {token}'}

        payload={}
        skip_keys = {"username"}
        for key, data in user_data.model_dump(exclude_unset=True).items():
            if key in skip_keys:
                continue
            payload[key] = data
        
        response: Response = requests.patch(url, headers=headers, data=payload)
        
        if response.status_code != 200:
            logger.error(f"Auth0 update failed: {response.content}")
            detail = response.json().get("message", "Error deleting user from authentication provider.")
            raise HTTPException(status_code=response.status_code, detail=detail)
