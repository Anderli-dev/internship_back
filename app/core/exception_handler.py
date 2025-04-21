from fastapi.responses import JSONResponse
from core.exceptions import Auth0Error, InvalidToken
from core.logger import logger
from fastapi import FastAPI, Request, status
from jose import JWTError, exceptions, jwt


def register_exception_handlers(app: FastAPI):
    
    @app.exception_handler(Exception)
    async def iternal_server_error(request: Request, exc: Exception):
        logger.exception(f"Error: {exc}")
        raise JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail":"Internal server error"})
    
    @app.exception_handler(exceptions.ExpiredSignatureError)        
    async def token_expired_handler(request: Request, exc: exceptions.ExpiredSignatureError):
        logger.error("Token expired!")
        raise JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail":"Token expired!"})

    @app.exception_handler(jwt.JWTClaimsError)   
    async def token_claims_error(request: Request, exc: jwt.JWTClaimsError):
        logger.error("Invalid token claims.")
        raise JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail":"Invalid claims!"})

    @app.exception_handler(InvalidToken)   
    def invalid_token_handler(request: Request, exc: InvalidToken):
        logger.error("Invalid token!")
        raise JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": "Invalid token!"})

    @app.exception_handler(JWTError)   
    def JWT_error_handler(request: Request, exc: JWTError):
        logger.error("Token error!")
        raise JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": "Token error!"})

    @app.exception_handler(Auth0Error)   
    def auth0_error_handler(request: Request, exc: Auth0Error):
        logger.error("Auth0 error!")
        detail = exc.detail
        if not exc.detail:
            detail = "Auth0 error!"
        raise JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": detail })