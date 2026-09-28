from fastapi import HTTPException, status


class BaseHTTPException(HTTPException):
    """ Base for all app-specific HTTP errors """

# Global Exception

class InvalidCredentialsError(BaseHTTPException):
    
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )


# Email Service Exception

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