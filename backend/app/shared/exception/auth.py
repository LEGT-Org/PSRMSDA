from app.shared.exception.base import BaseHTTPException


class InvalidRefreshTokenError(BaseHTTPException):
    
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

class NoRefreshTokenError(BaseHTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No refresh token"
        )

class ExpiredRefreshTokenError(BaseHTTPException):
    
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Expired refresh token"
        )