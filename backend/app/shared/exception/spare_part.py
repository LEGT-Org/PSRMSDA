from fastapi import status

from app.shared.exception.base import BaseHTTPException


class SparePartUpdateQuantityError(BaseHTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Spare part stock quantity failed to update"
        )


class SparePartDoesNotExistError(BaseHTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Spare part not found"
        )


class SparePartPartCodeAlreadyExistError(BaseHTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="This part code already exist"
        )


class SparePartUpdateRequestFailedError(BaseHTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="At least one field with a value must be provided"
        )


class SparePartInsufficientQuantityError(BaseHTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Insufficient spare part stock"
        )


class SparePartCreationFailedError(BaseHTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Spare part creation has failed"
        )


class SparePartUpdateFailedError(BaseHTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Spare part update has failed"
        )


class SparePartDeletionFailedError(BaseHTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Spare part deletion has failed"
        )