from fastapi import status

from app.shared.exception.base import BaseHTTPException


class CustomerDoesNotExistError(BaseHTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Customer does not exist"
        )


class CustomerValidationError(BaseHTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="At least one valid field must be provided"
        )


class CustomerCreationFailedError(BaseHTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Customer creation has failed"
        )


class CustomerUpdateFailedError(BaseHTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Customer update has failed"
        )


class CustomerDeleteFailedError(BaseHTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Customer deletion has failed"
        )