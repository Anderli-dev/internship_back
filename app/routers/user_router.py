from core.logger import logger
from db.schemas.UserSchema import (
    UserDetailResponse,
    UserSignUp,
    UsersListResponse,
    UserUpdate,
)
from db.session import get_db
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy.ext.asyncio import AsyncSession
from services.user_service import UserRepository
from utils.hash_password import hash_password

router = APIRouter(prefix="/users", tags=["users"])


@cbv(router)
class UserCBV:
    db: AsyncSession = Depends(get_db)

    @router.get("/", response_model=UsersListResponse)
    async def get_all_users(self):
        service = UserRepository(self.db)
        users = await service.get_all()
        total = len(users)

        if not users:
            logger.debug("No users in db!")
            return Response(status_code=204)

        logger.debug("Getting all users successful")
        return UsersListResponse(users=users, total=total)

    @router.post("/")
    async def create_user(self, user: UserSignUp):
        user.password = hash_password(user.password)
        service = UserRepository(self.db)
        new_user = await service.create(user)

        if new_user is None:
            raise HTTPException(status_code=400, detail="User creation failed!")

        logger.debug("Creating user successful")
        return new_user

    @router.get("/{user_id}", response_model=UserDetailResponse)
    async def get_user(self, user_id: int):
        service = UserRepository(self.db)
        user = await service.get_user(user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        logger.debug("Getting user successful")
        return UserDetailResponse.model_validate(user.__dict__)

    @router.put("/{user_id}", response_model=UserUpdate)
    async def update_user(self, user_id: int, user_data: UserUpdate):
        service = UserRepository(self.db)
        updated_user = await service.update(
            user_id,
            user_data.model_dump(exclude_unset=True)
        )

        logger.debug("Updating user successful")
        return UserDetailResponse.model_validate(updated_user.__dict__)

    @router.delete("/{user_id}")
    async def delete_user(self, user_id: int):
        logger.debug("Deleting user successful")
        service = UserRepository(self.db)
        return await service.delete(user_id)
