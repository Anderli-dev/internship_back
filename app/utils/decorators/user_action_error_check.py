import functools

from sqlalchemy import select

from db.models.user import User
from core.logger import logger
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


def user_action_error_check(secur: bool = False):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(
            self,
            db: AsyncSession,
            *args,
            **kwargs
        ):                
            if "user_email" not in kwargs["payload"]:
                logger.error("User email missing from payload.")
                raise HTTPException(status_code=400, detail="Invalid authentication payload.")

            user = await db.execute(select(User).filter(User.email == kwargs["payload"]["user_email"]))
            user = user.scalars().first()
            if not user:
                logger.error("User not found!")
                raise HTTPException(status_code=404, detail="User not found!")
            
            if secur:
                if kwargs["payload"]["user_email"] != user.email:
                    logger.warning(f"Unauthorized attempt by user {user.email} for user ID: {kwargs['user_email']}")
                    raise HTTPException(status_code=403, detail="Permission denied.")

            kwargs["user"] = user

            return await func(self, db, *args, **kwargs)

        return wrapper
    return decorator
