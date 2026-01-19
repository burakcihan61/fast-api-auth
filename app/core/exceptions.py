"""Custom exception classes"""


class AppException(Exception):
    """Base exception for application errors"""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class NotFoundException(AppException):
    """Resource not found exception"""

    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404)


class UnauthorizedException(AppException):
    """Unauthorized access exception"""

    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, status_code=401)


class ForbiddenException(AppException):
    """Forbidden access exception"""

    def __init__(self, message: str = "Forbidden"):
        super().__init__(message, status_code=403)


class BadRequestException(AppException):
    """Bad request exception"""

    def __init__(self, message: str = "Bad request"):
        super().__init__(message, status_code=400)


class ValidationException(AppException):
    """Validation error exception"""

    def __init__(self, message: str = "Validation error"):
        super().__init__(message, status_code=422)
