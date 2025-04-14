from core.logger import logger
from db.schemas.UserSchema import (UserDetailResponse, UserSignUp,
                                   UsersListResponse, UserUpdate)
from db.session import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.schemas.UserSchema import (UserDetailResponse, UserSignUp,
                                   UsersListResponse, UserUpdate)
from db.session import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from services.user_service import UserService
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=UsersListResponse)
async def get_all_users(db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    try:
        users, total = await service.get_all_users()
        return UsersListResponse(users=users, total=total)
    except Exception as e:
        logger.exception(f"Failed to fetch users: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.post("/", response_model=UserDetailResponse)
async def create_user(user: UserSignUp, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    try:
        new_user = await service.create_user(user)
        if not new_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User creation failed",
            )
        return new_user
    except Exception as e:
        logger.exception(f"Failed to create user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get("/{user_id}", response_model=UserDetailResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    try:
        user = await service.get_user(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user
    except Exception as e:
        logger.exception(f"Failed to fetch user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.put("/{user_id}", response_model=UserDetailResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_db),
):
    service = UserService(db)
    try:
        updated_user = await service.update_user(user_id, user_data)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return updated_user
    except Exception as e:
        logger.exception(f"Failed to update user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.delete("/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    try:
        deleted = await service.delete_user(user_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return {"message": "User deleted successfully"}
    except Exception as e:
        logger.exception(f"Failed to delete user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
