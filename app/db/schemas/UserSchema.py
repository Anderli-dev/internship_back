from typing import List, Optional
from pydantic import BaseModel, ConfigDict, EmailStr, field_validator


class UserBase(BaseModel):
    username: str
    email: EmailStr
    
    @field_validator("email")
    def normalize_email(cls, value: str) -> str:
        return value.lower()
    
class UserSignUp(UserBase):
    password: str
    
    @field_validator("password")
    def validate_password(cls, value: str) -> str:
        if len(value) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return value
    
class UserSignIn(BaseModel):
    email: EmailStr
    password: str
    
    @field_validator("password")
    def validate_password(cls, value: str) -> str:
        if len(value) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return value
    
    
class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    
class UsersListResponse(BaseModel):
    users: List[UserBase]
    total: int
    
class UserDetailResponse(UserBase):
    id: int
    
    model_config = ConfigDict(arbitrary_types_allowed=True)
