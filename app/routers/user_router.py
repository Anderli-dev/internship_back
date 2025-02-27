from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
async def get_all_users():
    pass

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