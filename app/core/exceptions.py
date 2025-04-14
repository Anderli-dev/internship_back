from core.logger import logger
from fastapi import HTTPException
from jose import exceptions
from fastapi import Request, status

class InvalidToken(Exception):
    def __init__(self, name: str):
        self.name = name
        
def token_expired_handler(request: Request, exc: exceptions.ExpiredSignatureError):
    logger.error("Token expired!")
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired!")

def invalid_token_handler(request: Request, exc: exceptions.ExpiredSignatureError):
    logger.error("Invalid token!")
    raise HTTPException(status_code=401, detail="Invalid token!")