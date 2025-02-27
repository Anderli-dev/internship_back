from fastapi import APIRouter, Depends, HTTPException, Response
from db.schemas.UserSchema import UsersListResponse
from db.session import get_db
from services.user_service import get_users
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=UsersListResponse)
async def get_all_users(db: AsyncSession = Depends(get_db)):
    users = await get_users(db)
    
    if not users:
        return Response(status_code=204)
    
    return users

@router.post("/")
async def create_user():
    pass

@router.get("/{user_id}")
async def get_user():
    pass

@router.put("/{user_id}")
async def update_user():
    pass

@router.delete("/{user_id}")
async def delete_user():
    pass