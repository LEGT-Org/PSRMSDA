from fastapi import status

from app.shared.exception.base import BaseHTTPException


class ProcurementAlertDoesNotExistError(BaseHTTPException):

    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )


class ProcurementAlertIsAlreadyBeenResolvedError(BaseHTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Procurement alert has been resolved"
        )


class ProcurementAlertFailedError(BaseHTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Procurement alert has failed"
        )

