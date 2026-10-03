from fastapi import status

from app.shared.exception.base import BaseHTTPException


class CustomerDoesNotExistError(BaseHTTPException):

    def __init__():
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Customer does not exist"
        )