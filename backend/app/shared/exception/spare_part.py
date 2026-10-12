from fastapi import status

from app.shared.exception.base import BaseHTTPException


class SparePartUpdateQuantityError(BaseHTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Spare part stock quantity failed to update"
        )


class SparePartInsufficientQuantityError(BaseHTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Insufficient spare part stock"
        )