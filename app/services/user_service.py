import asyncio
import jwt
from core.settings import SECRET_KEY, logger
from db.models import User
from db.schemas.UserSchema import UserBase, UserSignUp, UserUpdate
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from services.auth import ALGORITHM


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 10):
    logger.debug("Getting all users")
    users = await db.execute(select(User).offset(skip).limit(limit))
    users = users.scalars().all()
    users = [UserBase.model_validate(user.__dict__) for user in users] # Creating list of UserBase
    
    return users

async def read_user(user_id: int, db: AsyncSession):
    logger.debug("Getting user")
    user = await db.execute(select(User).filter(User.id == user_id))
    user = user.scalars().first()
    
    if not user:
        logger.error("User not found!")
        raise HTTPException(status_code=404, detail="User not found!")
    
    return user

async def create_new_user(user: UserSignUp, db: AsyncSession):
    logger.debug("Checking if user exists")
    result = await db.execute(select(User).where((User.email == user.email) | (User.username == user.username)))
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email or username already exists")
    
    logger.debug("Creating user")
    db_user = User(username=user.username, email=user.email, password=user.password)
    
    logger.debug("Adding user to db")
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    
    return db_user

async def update_user_data(user_id: int, user_data: UserUpdate, db: AsyncSession):
    logger.debug("Updating user")
    user = await db.execute(select(User).filter(User.id == user_id))
    user = user.scalars().first()
    
    if not user:
        logger.error("User not found!")
        raise HTTPException(status_code=404, detail="User not found!")
    
    logger.debug("Setting up user data")
    # Updating not None fields
    for key, data in user_data.items():
        setattr(user, key, data)
    
    logger.debug("Saving new user data in db")
    await db.commit()
    await db.refresh(user)
    
    return user
    

async def user_delete(user_id: int, db: AsyncSession):
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

async def token_get_me(token: str, db: AsyncSession):
    logger.debug("Getting user by token")
    try:
        loop = asyncio.get_running_loop()
        decoded_jwt = await loop.run_in_executor(None, jwt.decode, token, SECRET_KEY, ALGORITHM)
        
        user_email = decoded_jwt.get("user_email")
        if user_email is None:
            raise HTTPException(status_code=401, detail="Invalid token!")
        
        user = await db.execute(select(User).filter(User.email == decoded_jwt.get("user_email")))
        user = user.scalars().first()
        
        if not user:
            logger.error("User not found!")
            raise HTTPException(status_code=404, detail="User not found!")
        
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired!")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token!")
    except Exception as e:
        print(e)