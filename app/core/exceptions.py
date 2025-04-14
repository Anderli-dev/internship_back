from core.logger import logger
from fastapi import HTTPException
from jose import JWTError, exceptions
from fastapi import Request, status
from jose import jwt

class InvalidToken(JWTError):
    def __init__(self, name: str):
        self.name = name
        
def token_expired_handler(request: Request, exc: exceptions.ExpiredSignatureError):
    logger.error("Token expired!")
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired!")

def token_claims_error(request: Request, exc: jwt.JWTClaimsError):
    logger.error("Invalid token claims.")
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid claims!")

def invalid_token_handler(request: Request, exc: InvalidToken):
    logger.error("Invalid token!")
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token!")