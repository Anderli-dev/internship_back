from core.logger import logger
from db.schemas.user_schema import (UserDetailResponse, UserSignUp,
                                   UsersListResponse, UserUpdate)
from db.session import get_db
from fastapi import APIRouter, Depends, Response
from services.auth import Auth
from services.user_service.create import UserCreateService
from services.user_service.delete import UserDeleteService
from services.user_service.read import UserReadService
from services.user_service.update import UserUpdateService
from sqlalchemy.ext.asyncio import AsyncSession
from utils.hash_password import hash_password

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=UsersListResponse)
async def get_all_users(db: AsyncSession = Depends(get_db)) -> UsersListResponse:
    logger.info("Getting all users.")
    
    users = await UserReadService.get_all_users(db)
    total = len(users)
    
    if not users:
        logger.debug("No users in db!")
        return Response(status_code=204)
    
    logger.debug("Getting all users successful")
    return UsersListResponse.model_validate({"users": users, "total": total})

@router.post("/")
async def create_user(user: UserSignUp, db: AsyncSession = Depends(get_db)) -> UserSignUp:
    logger.info("Creating user.")
    
    user.password = hash_password(user.password)
    user = await UserCreateService.create_user(user, db)
    
    if user is None:
        logger.error("User creation failed!")
        return Response(status_code=204, detail="User creation failed!")
    
    logger.info("Creating user successful")
    return user
    
@router.get("/{user_id}", response_model=UserDetailResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)) -> UserDetailResponse:
    logger.info("Getting user info.")
    
    service = UserReadService()
    user = await service.read_user_from_db(db, user_id)
    
    logger.info("Getting user successful")
    return UserDetailResponse.model_validate(user.__dict__)

@router.put("/{user_id}", response_model=UserDetailResponse)
async def update_user(user_data: UserUpdate, db: AsyncSession = Depends(get_db), payload: dict = Depends(Auth().get_token_payload)) -> UserDetailResponse:
    logger.info("Updating user.")
    
    service = UserUpdateService()
    user = await service.update_user(db, user_data, payload=payload)
    
    return UserDetailResponse.model_validate(user.__dict__)

@router.delete("/{user_id}")
async def delete_user(db: AsyncSession = Depends(get_db), payload: dict = Depends(Auth().get_token_payload)) -> dict:
    logger.info(f"Request to delete user")
    
    service = UserDeleteService()
    
    return await service.delete_user(db, payload=payload)

@router.get("/me/", response_model=UserDetailResponse)
async def get_me(db: AsyncSession = Depends(get_db), payload: dict = Depends(Auth().get_token_payload)) -> UserDetailResponse:
    logger.info("Getting information about me.")
    
    user = await UserReadService().read_auth_user(db, payload=payload)
    
    return UserDetailResponse.model_validate(user.__dict__)
