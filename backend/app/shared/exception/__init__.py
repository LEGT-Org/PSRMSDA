from app.shared.exception.base import (
    InvalidCredentialsError, 
    BaseHTTPException,  
)

from app.shared.exception.email_service import (
    EmailServiceAuthenticationError,
    EmailServiceUnavailableError,
    EmailMustContainBodyOrHTML,
    RecipientIsRequiredError,
    EmailServiceFailedError,
    SubjectIsRequiredError
)

from app.shared.exception.llm_service import (
    LLMDiagnosticFaultsMustStartWithOneError,
    LLMDiagnosticHypothesesNonExistentError,
    LLMDiagnosisInvalidListOfStringError,
    LLMDiagnosisInvalidStringError,
    LLMServiceAuthenticationError,
    LLMServiceUnavailableError,
    LLMServiceRateLimitError,
    LLMServiceContentError,
    LLMServiceTimeoutError
)

from app.shared.exception.service_request import (
    ServiceRequestStatusIsNotPendingError,
    ServiceRequestDoesNotExistError,
    ServiceRequestFailedError
)

from app.shared.exception.procurement_alert import (
    ProcurementAlertFailedError
)

from app.shared.exception.request_part import (
    RequestPartFailedError
)

from app.shared.exception.customer import (
    CustomerDoesNotExistError    
)

from app.shared.exception.category import (
    CategoryDoesNotExistError
)

from app.shared.exception.auth import (
    ExpiredRefreshTokenError, 
    InvalidRefreshTokenError, 
    NoRefreshTokenError
)

from app.shared.exception.user import (
    NameOnlyContainAlphabeticCharacterError, 
    NameMustBeTwoToFiftyCharacterError,
    PasswordMustContainLowercaseError,
    PasswordMustContainUppercaseError,
    PasswordMustContainNumberError, 
    InvalidRegistrationTokenError, 
    PasswordDoesNotMatchError,
    InvalidEmailAddressError, 
    InvalidPhoneNumberError,
    EmailAlreadyExistsError,
    EmailServiceFailedError,
    SetupNewPasswordError,
    NoNameError
)  



__all__ = [

    # Global Exception
    "InvalidCredentialsError",

    # Registration Exception
    "PasswordMustContainLowercaseError",
    "PasswordMustContainUppercaseError",
    "PasswordMustContainNumberError",
    "InvalidRegistrationTokenError",
    "SetupNewPasswordError",
    "PasswordDoesNotMatch",

    # Email Service Exception
    "EmailServiceAuthenticationError",
    "EmailServiceUnavailableError",
    "EmailMustContainBoryOrHTML",
    "RecipientIsRequiredError", 
    "EmailServiceFailedError",
    "SubjectIsRequiredError",

    # LLM Service Exception
    "LLMServiceAuthenticationError",
    "LLMServiceUnavailableError",
    "LLMServiceRateLimitError",
    "LLMServiceContentError",
    "LLMServiceTimeoutError", 

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
    "InvalidPhoneNumberError", 
    "NoNameError",

    # LLM Diagnosis Exception
    "LLMDiagnosticFaultsMustStartWithOneError",
    "LLMDiagnosticHypothesesNonExistentError",
    "LLMDiagnosisInvalidListOfStringError",
    "LLMDiagnosisInvalidStringError",

    # Service Request Exception
    "ServiceRequestStatusIsNotPendingError",
    "ServiceRequestDoesNotExistError",
    "ServiceRequestFailedError",

    # Customer Exception
    "CustomerDoesNotExistError",

    # Category Exception
    "CategoryDoesNotExistError",

    # Request Part Exception
    "RequestPartFailedError",

    # Procurement Alert Exception
    "ProcurementAlertFailedError",
    
]