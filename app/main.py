from routers import db_router
import core.settings as settings

import uvicorn


from db.session import get_db

from fastapi import Depends, FastAPI

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from utils.cors import add_cors_middleware

app = FastAPI()

add_cors_middleware(app)

app.include_router(db_router.router)

@app.get("/")
async def home() -> dict:
    return {"status_code": 200, "detail": "ok", "result": "working"}
    
if __name__ == "__main__":
    # To make the work more comfortable, you can run a script. 
    # It is better to do this in a separate file like run.py.
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
    