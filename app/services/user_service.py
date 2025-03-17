from core.logger import logger
from db.models import User
from db.schemas.UserSchema import (UserBase, UserSignUp,
                                   UserUpdate)
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from utils.hash_password import hash_password



async def get_users(db: AsyncSession, skip: int = 0, limit: int = 10) -> list[UserBase]:
    logger.debug("Getting all users")
    users = await db.execute(select(User).offset(skip).limit(limit))
    users = users.scalars().all()
    users = [UserBase.model_validate(user.__dict__) for user in users] # Creating list of UserBase
    
    return users

async def read_user(user_id: int, db: AsyncSession) -> User:
    logger.debug("Getting user")
    user = await db.execute(select(User).filter(User.id == user_id))
    user = user.scalars().first()
    
    if not user:
        logger.error("User not found!")
        raise HTTPException(status_code=404, detail="User not found!")
    
    return user

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
