import functools

from core.logger import logger
from fastapi import HTTPException
from jose import exceptions


def token_exception_check(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except exceptions.ExpiredSignatureError:
            logger.error("Token expired!")
            raise HTTPException(status_code=401, detail="Token expired!")
        except exceptions.JWEInvalidAuth:
            logger.error("Invalid token!")
            raise HTTPException(status_code=401, detail="Invalid token!")
        except exceptions.JWTError:
            logger.error("Auth0 invalid token.")
            raise HTTPException(status_code=401, detail="Invalid token")
        except Exception as e:
            logger.error(f"Token error: {e}")
            raise HTTPException(status_code=401, detail="Token error!")
    return wrapper