from fastapi import status

from app.shared.exception.base import BaseHTTPException


class RecipientIsRequiredError(BaseHTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Recipient is required"
        )


class SubjectIsRequiredError(BaseHTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Subject is required"
        )
        

class EmailMustContainBodyOrHTML(BaseHTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email must contain either body or HTML"
        )


class EmailServiceFailedError(BaseHTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="The Email service failed to connect"
        )


class EmailServiceUnavailableError(BaseHTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The Email service is currently unavailable"
        )


class EmailServiceAuthenticationError(BaseHTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The Email service credentials is failing"
        )