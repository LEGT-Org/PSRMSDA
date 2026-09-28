from app.shared.exception.base import (
    EmailMustContainBodyOrHTML,
    RecipientIsRequiredError, 
    InvalidCredentialsError, 
    SubjectIsRequiredError,
    BaseHTTPException,  
)

from app.shared.exception.auth import (
    ExpiredRefreshTokenError, 
    InvalidRefreshTokenError, 
    NoRefreshTokenError
)

from app.shared.exception.user import (
    NameOnlyContainAlphabeticCharacterError, 
    NameMustBeTwoToFiftyCharacterError, 
    InvalidEmailAddressError, 
    EmailAlreadyExistsError,
    EmailServiceFailedError, 
    NoNameError
)  



__all__ = [

    # Global Exception
    "InvalidCredentialsError",

    # Email Service Exception
    "RecipientIsRequiredError", 
    "SubjectIsRequiredError", 
    "EmailMustContainBoryOrHTML",

    # Auth Exception
    "ExpiredRefreshTokenError",
    "InvalidRefreshTokenError", 
    "NoRefreshTokenError",

    # User Exception
    "NameOnlyContainAlphabeticCharacterError", 
    "NameMustBeTwoToFiftyCharacterError", 
    "InvalidEmailAddressError", 
    "EmailAlreadyExistsError",
    "EmailServiceFailedError", 
    "NoNameError",
]