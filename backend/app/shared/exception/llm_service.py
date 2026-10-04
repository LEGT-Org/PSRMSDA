from fastapi import status

from app.shared.exception.base import BaseHTTPException


class LLMServiceContentError(BaseHTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The LLM service return empty content"
        )


class LLMServiceAuthenticationError(BaseHTTPException):
    
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The LLM service API key is failing"
        )


class LLMServiceTimeoutError(BaseHTTPException):
    
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="The LLM service timed out"
        )


class LLMServiceRateLimitError(BaseHTTPException):
    
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="The LLM API service is temporarily rate limited"
        )


class LLMServiceUnavailableError(BaseHTTPException):
    
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The LLM service is currently unavailable"
        )


class LLMDiagnosisInvalidStringError(BaseHTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="String value cannot be empty"
        )


class LLMDiagnosisInvalidListOfStringError(BaseHTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Fault descriptions cannot be empty"
        )


class LLMDiagnosticFaultsMustStartWithOneError(BaseHTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=(
                "Supporting fault numbers must "
                "start at 1."
            )
        )


class LLMDiagnosticHypothesesNonExistentError(BaseHTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=(
                "A hypothesis references a "
                "non-existent fault."
            )
        )

