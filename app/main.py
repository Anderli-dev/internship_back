import uvicorn
from app.core.exception_handler import register_exception_handlers
from core.settings import settings
from fastapi import FastAPI
from routers import auth_router, db_router, user_router
from utils.cors import add_cors_middleware

app = FastAPI()

add_cors_middleware(app)

register_exception_handlers(app)

app.include_router(db_router.router)
app.include_router(user_router.router)
app.include_router(auth_router.router)

@app.get("/")
def home() -> dict:
    return {"status_code": 200, "detail": "ok", "result": "working"}
    
if __name__ == "__main__":
    # To make the work more comfortable, you can run a script. 
    # It is better to do this in a separate file like run.py.
    uvicorn.run("main:app", host=settings.app_host, port=settings.app_port, reload=True)
    