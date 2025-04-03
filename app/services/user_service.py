from typing import Optional

from db.schemas.UserSchema import (UserBase, UserDetailResponse, UserSignUp,
                                   UserUpdate)
from repositories.user_repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from utils.hash_password import hash_password


class UserService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)

    async def get_all_users(self) -> tuple[list[UserBase], int]:
        users = await self.repo.get_all()
        return users, len(users)

    async def create_user(self, user: UserSignUp) -> Optional[UserDetailResponse]:
        user.password = hash_password(user.password)
        new_user = await self.repo.create(user)
        if not new_user:
            return None
        return UserDetailResponse.model_validate(new_user.__dict__)

    async def get_user(self, user_id: int) -> Optional[UserDetailResponse]:
        user = await self.repo.get_user(user_id)
        if not user:
            return None
        return UserDetailResponse.model_validate(user.__dict__)

    async def update_user(self, user_id: int, user_data: UserUpdate) -> UserDetailResponse | None:
        updated_user = await self.repo.update(user_id, user_data.model_dump(exclude_unset=True))
        if not updated_user:
            return None
        return UserDetailResponse.model_validate(updated_user.__dict__)

    async def delete_user(self, user_id: int) -> bool:
        return await self.repo.delete(user_id)
