from fastapi import status

from app.shared.exception.base import BaseHTTPException


class ServiceRequestDoesNotExistError(BaseHTTPException):

    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )

class ServiceRequestStatusIsNotPendingError(BaseHTTPException):

    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=detail
        )
        

class ServiceRequestStatusCanOnlyBeCompletedOrUnsuccessfulError(BaseHTTPException):

    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=detail
        )


class ServiceRequestStatusCanOnlyModifiedAgainError(BaseHTTPException):

    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )


class ServiceRequestFailedError(BaseHTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service request confirmation has failed"
        )