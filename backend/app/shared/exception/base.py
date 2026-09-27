from fastapi import HTTPException, status


class BaseHTTPException(HTTPException):
    """ Base for all app-specific HTTP errors """

class InvalidCredentialsError(BaseHTTPException):
    
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )