# src/utils/exceptions.py

# This module defines custom exceptions for the application.

class APIException(Exception):
    """Base class for API exceptions."""
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)

class LLMConnectionError(APIException):
    """Raised when unable to connect to the LLM service."""
    def __init__(self, detail: str = "Could not connect to the LLM service."):
        super().__init__(status_code=503, detail=detail) # 503 Service Unavailable

class InvalidRequestError(APIException):
    """Raised for invalid client requests."""
    def __init__(self, detail: str = "Invalid request payload."):
        super().__init__(status_code=400, detail=detail) # 400 Bad Request