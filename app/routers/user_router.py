from fastapi import APIRouter, Depends, HTTPException, Response
from utils.hash_password import hash_password
from db.schemas.UserSchema import UserSignUp, UsersListResponse, UserDetailResponse, UserUpdate
from db.session import get_db
from services.user_service import get_users, create_new_user, read_user, update_user_data
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
    
    if user is None:
        return Response(status_code=204, detail="User creation failed!")
    
    return user
    

@router.get("/{user_id}", response_model=UserDetailResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await read_user(user_id, db)
    
    return UserDetailResponse.model_validate(user.__dict__)

@router.put("/{user_id}", response_model=UserUpdate)
async def update_user(user_id: int, user_data: UserUpdate, db: AsyncSession = Depends(get_db)):
    user = await update_user_data(user_id, user_data.model_dump(exclude_unset=True), db)
    
    return UserDetailResponse.model_validate(user.__dict__)

@router.delete("/{user_id}")
async def delete_user():
    pass