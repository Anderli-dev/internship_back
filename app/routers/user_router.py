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
        try:
            service = UserRepository(self.db)
            users = await service.get_all()
            total = len(users)

            if not users:
                logger.debug("No users in db!")
                return Response(status_code=204)

            logger.debug("Getting all users successful")
            return UsersListResponse(users=users, total=total)
        except Exception as e:
            logger.exception("Failed to get all users")
            raise HTTPException(status_code=500, detail="Internal server error")

    @router.post("/")
    async def create_user(self, user: UserSignUp):
        try:
            user.password = hash_password(user.password)
            service = UserRepository(self.db)
            new_user = await service.create(user)

            if new_user is None:
                raise HTTPException(status_code=400, detail="User creation failed!")

            logger.debug("Creating user successful")
            return new_user
        except Exception:
            logger.exception("Unexpected error during user creation")
            raise HTTPException(status_code=500, detail="Internal server error")

    @router.get("/{user_id}", response_model=UserDetailResponse)
    async def get_user(self, user_id: int):
        try:
            service = UserRepository(self.db)
            user = await service.get_user(user_id)
            logger.debug("Getting user successful")
            return UserDetailResponse.model_validate(user.__dict__)
        except Exception:
            logger.exception("Unexpected error during user fetch")
            raise HTTPException(status_code=500, detail="Internal server error")

    @router.put("/{user_id}", response_model=UserUpdate)
    async def update_user(self, user_id: int, user_data: UserUpdate):
        try:
            service = UserRepository(self.db)
            updated_user = await service.update(
                user_id,
                user_data.model_dump(exclude_unset=True)
            )
            logger.debug("Updating user successful")
            return UserDetailResponse.model_validate(updated_user.__dict__)
        except Exception:
            logger.exception("Unexpected error during user update")
            raise HTTPException(status_code=500, detail="Internal server error")

    @router.delete("/{user_id}")
    async def delete_user(self, user_id: int):
        try:
            service = UserRepository(self.db)
            deleted = await service.delete(user_id)
            if not deleted:
                logger.warning(f"User with ID {user_id} not found")
                raise HTTPException(status_code=404, detail="User not found")

            logger.debug(f"User with ID {user_id} deleted successfully")
            return {"message": "User deleted successfully"}
        except Exception:
            logger.exception("Unexpected error during user deletion")
            raise HTTPException(status_code=500, detail="Internal server error")

