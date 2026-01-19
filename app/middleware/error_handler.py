"""Global exception handler middleware"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.exceptions import AppException


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    """Middleware to handle custom exceptions globally"""

    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except AppException as exc:
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "success": False,
                    "message": exc.message,
                    "error_code": type(exc).__name__,
                },
            )
        except Exception as exc:
            # Log the exception here
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "success": False,
                    "message": "Internal server error",
                    "error_code": "InternalServerError",
                },
            )
