from core.logger import logger
from fastapi import HTTPException, Request, status
from jose import JWTError, exceptions, jwt


class InvalidToken(JWTError):
    def __init__(self, name: str):
        self.name = name
        
class Auth0Error(Exception):
    def __init__(self, detail: str):
        self.detail = detail
        
def iternal_server_error(request: Request, exc: Exception):
    logger.exception(f"Error: {exc}")
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Internal server error")
        
def token_expired_handler(request: Request, exc: exceptions.ExpiredSignatureError):
    logger.error("Token expired!")
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired!")

def token_claims_error(request: Request, exc: jwt.JWTClaimsError):
    logger.error("Invalid token claims.")
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid claims!")

def invalid_token_handler(request: Request, exc: InvalidToken):
    logger.error("Invalid token!")
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token!")

def JWT_error_handler(request: Request, exc: JWTError):
    logger.error("Token error!")
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token error!")

def auth0_error_handler(request: Request, exc: Auth0Error):
    logger.error("Auth0 error!")
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = exc.detail | "Auth0 error!")
