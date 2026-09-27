from app.shared.exception.base import BaseHTTPException


class EmailAlreadyExistsError(Exception):
    
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )

class InvalidEmailAddressError(Exception):
    
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Invalid email address"
        )

class NoNameError(Exception):
    
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Name cannot be empty"
        )


class NameMustBeTwoToFiftyCharacterError(Exception):
    
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Name must be 2 to 50 characters only"
        )

class NameOnlyContainAlphabeticCharacterError(Exception):
    
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Name can only contain alphabetic characters, spaces, hypens, and apostrophes"
        )


class EmailServiceFailedError(Exception):
    
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Email Service Failed"
        )