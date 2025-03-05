from core.settings import logger
from db.schemas.UserSchema import (UserBase, UserDetailResponse, UserSignUp,
                                   UsersListResponse, UserUpdate)
from db.session import get_db
from fastapi import APIRouter, Depends, HTTPException, Response
from services.auth0 import verify_jwt
from services.user_service import (create_new_user, get_users, read_user,
                                   token_get_me, update_user_data, user_delete)
from sqlalchemy.ext.asyncio import AsyncSession
from utils.hash_password import hash_password

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=UsersListResponse)
async def get_all_users(db: AsyncSession = Depends(get_db)) -> UsersListResponse:
    logger.info("Getting all users.")
    users = await get_users(db)
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
    user = await create_new_user(user, db)
    
    if user is None:
        logger.error("User creation failed!")
        return Response(status_code=204, detail="User creation failed!")
    
    logger.info("Creating user successful")
    return user
    
@router.get("/{user_id}", response_model=UserDetailResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)) -> UserDetailResponse:
    logger.info("Getting user info.")
    user = await read_user(user_id, db)
    
    logger.info("Getting user successful")
    return UserDetailResponse.model_validate(user.__dict__)

@router.put("/{user_id}", response_model=UserUpdate)
async def update_user(user_id: int, user_data: UserUpdate, db: AsyncSession = Depends(get_db)) -> UserDetailResponse:
    logger.info("Updating user.")
    user = await update_user_data(user_id, user_data.model_dump(exclude_unset=True), db) # user_data.model_dump(exclude_unset=True) for geting not None fields
    
    logger.info("Updating user successful.")
    return UserDetailResponse.model_validate(user.__dict__)

@router.delete("/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    logger.info("Deleting user successful.")
    return await user_delete(user_id, db)

@router.get("/me/", response_model=UserBase)
async def get_me(token: str, db: AsyncSession = Depends(get_db)) -> UserBase:
    logger.info("Getting information about yourself.")
    user = await token_get_me(token, db) 
    return UserBase.model_validate(user.__dict__)

@router.post("/me/auth0/")
async def auth0_me(data: dict = Depends(verify_jwt)) -> dict:
    # This endpoint protected by Auth0 token
    logger.info("Getting information about yourself Auth0.")
    if not data:
        logger.error("User incorrect username or password")
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    return {"message": "You have accessed a protected route!", "data": data}