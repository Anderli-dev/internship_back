import requests
from core.logger import logger
from core.settings import settings
from db.models import User
from db.schemas.UserSchema import UserBase, UserSignUp, UserUpdate
from fastapi import HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from utils.auth0.get_management_token import get_management_token
from utils.hash_password import hash_password


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 10) -> list[UserBase]:
    logger.debug("Getting all users")
    users = await db.execute(select(User).offset(skip).limit(limit))
    users = users.scalars().all()
    users = [UserBase.model_validate(user.__dict__) for user in users] # Creating list of UserBase
    
    return users

async def get_user_by_field(db: AsyncSession, field: str, value) -> User:
    logger.debug("Getting user")
    user = await db.execute(select(User).filter(getattr(User, field) == value))
    user = user.scalars().first()
    
    if not user:
        logger.error("User not found!")
        raise HTTPException(status_code=404, detail="User not found!")
    
    return user

async def get_me_user(email: str, db: AsyncSession) -> User:
    return await get_user_by_field(db, "email", email)

async def read_user(user_id: int, db: AsyncSession) -> User:
    return await get_user_by_field(db, "id", user_id)

async def create_new_user(user: UserSignUp, db: AsyncSession) -> User:
    logger.debug("Checking if user exists")
    result = await db.execute(select(User).where((User.email == user.email) | (User.username == user.username)))
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    
    logger.debug("Creating user")
    db_user = User(username=user.username, email=user.email, password=user.password)
    
    logger.debug("Adding user to db")
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    
    return db_user

async def update_user_data(user_id: int, user_data: UserUpdate, db: AsyncSession) -> User:
    logger.debug("Updating user")
    user = await db.execute(select(User).filter(User.id == user_id))
    user = user.scalars().first()
    
    if not user:
        logger.error("User not found!")
        raise HTTPException(status_code=404, detail="User not found!")
    
    logger.debug("Setting up user data")
    # Updating not None fields
    for key, data in user_data.items():
        if key == "password":
            data = hash_password(data)
        setattr(user, key, data)
    
    logger.debug("Saving new user data in db")
    await db.commit()
    await db.refresh(user)
    
    return user

async def user_delete_service(user_id: int, payload: dict, db: AsyncSession):
    if "user_email" not in payload:
        logger.error("User email missing from payload.")
        raise HTTPException(status_code=400, detail="Invalid authentication payload.")
    
    user = await get_me_user(payload["user_email"], db)
    
    if user_id != user.id:
        logger.warning(f"Unauthorized delete attempt by user {user.id} for user ID: {user_id}")
        raise HTTPException(status_code=403, detail="Permission denied.")
    
    if "sub" in payload:
        await auth0_user_delete(payload)
        
    return await user_delete(user_id, db)
    
async def user_delete(user_id: int, db: AsyncSession) -> dict:
    logger.debug("Deleting user")
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()

    if not user:
        logger.error("User not found!")
        raise HTTPException(status_code=404, detail="User not found!")

    logger.debug("Deleting user in db")
    await db.delete(user)
    await db.commit()

    return {"message": "User deleted successfully"}

async def auth0_user_delete(payload: dict) -> dict:
    token = await get_management_token()
    
    url = f'https://{settings.auth0_domain}/api/v2/users/{payload["sub"]}'
    headers = {'Authorization': f'Bearer {token}'}

    response: Response = requests.delete(url, headers=headers)
    
    if response.status_code != 204:
        logger.error(f"Auth0 deletion failed: {response.content}")
        detail = response.json().get("message", "Error deleting user from authentication provider.")
        raise HTTPException(status_code=response.status_code, detail=detail)