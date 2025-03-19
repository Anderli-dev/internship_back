import functools

from core.logger import logger
from fastapi import HTTPException
from services.user_service import get_me_user
from sqlalchemy.ext.asyncio import AsyncSession


def user_action_error_check(optional_user: bool = False):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(
            self,
            user_id: int,
            payload: dict,
            db: AsyncSession,
            *args,
            **kwargs
        ):
            if "user_email" not in payload:
                logger.error("User email missing from payload.")
                raise HTTPException(status_code=400, detail="Invalid authentication payload.")

            user = await get_me_user(payload["user_email"], db)
            if not user:
                logger.error("User not found!")
                raise HTTPException(status_code=404, detail="User not found!")
            
            if user_id != user.id:
                logger.warning(f"Unauthorized attempt by user {user.id} for user ID: {user_id}")
                raise HTTPException(status_code=403, detail="Permission denied.")

            if optional_user:
                kwargs["user"] = user

            return await func(self, user_id, payload, db, *args, **kwargs)

        return wrapper
    return decorator
