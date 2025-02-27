from fastapi import APIRouter, Depends, Response
from utils.hash_password import hash_password
from db.schemas.UserSchema import UserSignUp, UsersListResponse, UserBase
from db.session import get_db
from services.user_service import get_users, create_new_user
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=UsersListResponse)
async def get_all_users(db: AsyncSession = Depends(get_db)):
    users = await get_users(db)
    total = users.__sizeof__()
    
    if not users:
        return Response(status_code=204)
    
    return UsersListResponse.model_validate({"users": users, "total": total})

@router.post("/")
async def create_user(user: UserSignUp, db: AsyncSession = Depends(get_db)):
    user.password = hash_password(user.password)
    user = await create_new_user(user, db)

@router.get("/{user_id}")
async def get_user():
    pass

@router.put("/{user_id}")
async def update_user():
    pass

@router.delete("/{user_id}")
async def delete_user():
    pass