from fastapi import status

from app.shared.exception.base import BaseHTTPException

class EmailAlreadyExistsError(BaseHTTPException):
    
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )

class InvalidEmailAddressError(BaseHTTPException):
    
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Invalid email address"
        )

class NoNameError(BaseHTTPException):
    
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Name cannot be empty"
        )


class NameMustBeTwoToFiftyCharacterError(BaseHTTPException):
    
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Name must be 2 to 50 characters only"
        )

class NameOnlyContainAlphabeticCharacterError(BaseHTTPException):
    
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Name can only contain alphabetic characters, spaces, hypens, and apostrophes"
        )


class EmailServiceFailedError(BaseHTTPException):
    
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Email Service Failed"
        )


class InvalidRegistrationTokenError(BaseHTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid registration token"
        )


class SetupNewPasswordError(BaseHTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Registration failed"
        )


class PasswordMustContainUppercaseError(BaseHTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Password must contain an uppercase letter"
        )


class PasswordMustContainLowercaseError(BaseHTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Password must contain a lowercase letter"
        )


class PasswordMustContainNumberError(BaseHTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Password must contain a number"
        )


class PasswordDoesNotMatchError(BaseHTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Password and Confirm Password does not match"
        )