from core.logger import logger
from db.schemas.UserSchema import (UserDetailResponse, UserSignUp,
                                   UsersListResponse, UserUpdate)
from db.session import get_db
from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from services.auth_service import AuthService
from services.user_service import UserService
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=UsersListResponse)
async def get_all_users(db: AsyncSession = Depends(get_db)):
    logger.info("Getting users.")
    service = UserService(db)
    users, total = await service.get_all_users()
    return UsersListResponse(users=users, total=total)


@router.post("/", response_model=UserDetailResponse)
async def create_user(user: UserSignUp, db: AsyncSession = Depends(get_db)):
    logger.info("Creating user.")
    service = UserService(db)
    new_user = await service.create_user(user)
    if not new_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User creation failed")
    return new_user


@router.get("/{user_id}", response_model=UserDetailResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    logger.info("Getting user.")
    service = UserService(db)
    user = await service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserDetailResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_db),
):
    logger.info("Updating user.")
    service = UserService(db)
    updated_user = await service.update_user(user_id, user_data)
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    return updated_user


@router.delete("/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    logger.info("Deleting user.")
    service = UserService(db)
    deleted = await service.delete_user(user_id)
    if not deleted:
        logger.info("Failed to delete. User does not exist in db")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message": "User deleted successfully"}
        
security = HTTPBearer()
@router.get("/me/", response_model=UserDetailResponse)
async def get_me(credentials: HTTPAuthorizationCredentials = Security(security), db: AsyncSession = Depends(get_db)) -> UserDetailResponse:
    logger.info("Getting information about yourself.")
    service = AuthService(db)
    user = await service.get_current_user(credentials)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserDetailResponse.model_validate(user.__dict__)