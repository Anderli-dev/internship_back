from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_db
from db.schemas.UserSchema import UserSignUp, UserUpdate, UsersListResponse, UserDetailResponse
from services.user_service import UserService
from core.logger import logger

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=UsersListResponse)
async def get_all_users(db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    try:
        users, total = await service.get_all_users()
        if not users:
            logger.debug("No users in DB")
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        return UsersListResponse(users=users, total=total)
    except Exception as e:
        logger.exception(f"Failed to fetch users: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/", response_model=UserDetailResponse)
async def create_user(user: UserSignUp, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    try:
        new_user = await service.create_user(user)
        if not new_user:
            raise HTTPException(status_code=400, detail="User creation failed")
        return new_user
    except Exception as e:
        logger.exception(f"Failed to create user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{user_id}", response_model=UserDetailResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    try:
        user = await service.get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        logger.exception(f"Failed to fetch user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/{user_id}", response_model=UserDetailResponse)
async def update_user(user_id: int, user_data: UserUpdate, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    try:
        updated_user = await service.update_user(user_id, user_data)
        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")
        return updated_user
    except Exception as e:
        logger.exception(f"Failed to update user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    try:
        deleted = await service.delete_user(user_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deleted successfully"}
    except Exception as e:
        logger.exception(f"Failed to delete user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
