from fastapi import status

from app.shared.exception.base import BaseHTTPException


class RequestPartFailedError(BaseHTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Request part has failed"
        )