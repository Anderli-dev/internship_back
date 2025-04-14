import uvicorn
from core.settings import settings
from fastapi import FastAPI
from jose import exceptions, jwt
from routers import auth0_router, auth_router, db_router, user_router
from utils.cors import add_cors_middleware

from app.core.exceptions import (InvalidToken, invalid_token_handler,
                                 token_claims_error, token_expired_handler)

app = FastAPI()

add_cors_middleware(app)

app.add_exception_handler(exceptions.ExpiredSignatureError, token_expired_handler)
app.add_exception_handler(InvalidToken, invalid_token_handler)
app.add_exception_handler(jwt.JWTClaimsError, token_claims_error)

app.include_router(db_router.router)
app.include_router(user_router.router)
app.include_router(auth_router.router)
app.include_router(auth0_router.router)

@app.get("/")
def home() -> dict:
    print(settings.cors_origins)
    return {"status_code": 200, "detail": "ok", "result": "working"}
    
if __name__ == "__main__":
    # To make the work more comfortable, you can run a script. 
    # It is better to do this in a separate file like run.py.
    uvicorn.run("main:app", host=settings.app_host, port=settings.app_port, reload=True)
    