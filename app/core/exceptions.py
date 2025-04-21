from jose import JWTError


class InvalidToken(JWTError):
    def __init__(self, name: str):
        self.name = name
        
class Auth0Error(Exception):
    def __init__(self, detail: str):
        self.detail = detail
