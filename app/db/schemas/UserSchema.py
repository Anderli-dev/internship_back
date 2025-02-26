from typing import List, Optional
from pydantic import BaseModel, EmailStr
from sqlalchemy import UUID


class UserBase(BaseModel):
    username: str
    email: EmailStr
    
class UserSignUp(UserBase):
    password: str
    
class UserSignIn(BaseModel):
    email: EmailStr
    password: str
    
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    
class UsersListResponse(BaseModel):
    users: List[UserBase]
    total: int
    
class UserDetailResponse(UserBase):
    id: UUID