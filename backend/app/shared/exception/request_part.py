from fastapi import status

from app.shared.exception.base import BaseHTTPException


class RequestPartDuplicationError(BaseHTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Duplicate request part IDs"
        )


class RequestPartInvalidUsageConfirmationError(BaseHTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Every requested part must have a valid usage confirmation"
        )


class RequestPartQuantityUsedMustGreaterThanZeroError(BaseHTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Quantity used must be greater than zero when a part was used"
        )


class RequestPartQuantityUsedMustBeZeroError(BaseHTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Quantity used must be zero when no part was used"
        )


class RequestPartFailedError(BaseHTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Request part has failed"
        )