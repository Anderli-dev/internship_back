from sqlalchemy.ext.asyncio import AsyncSession
from db.models import User
from sqlalchemy.future import select

class AuthRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        
    async def get_user_by_email(self, user_email: str):
        user = await self.db.execute(select(User).filter(User.email == user_email))
        user = user.scalars().first()
        
        return user