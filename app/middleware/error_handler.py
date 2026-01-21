"""Global exception handler middleware"""

from collections.abc import Awaitable, Callable

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.exceptions import AppException


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    """Middleware to handle custom exceptions globally"""

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        try:
            response = await call_next(request)
            return response
        except AppException as exc:
            from app.core.i18n import t  # Import locally to avoid circular imports

            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "success": False,
                    "message": t(exc.message),
                    "error_code": type(exc).__name__,
                },
            )
        except Exception as e:
            # Log the exception here
            import traceback

            from app.core.logging import logger
            from app.core.i18n import t

            logger.error(f"Unhandled exception: {e}", extra={"traceback": traceback.format_exc()})
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "success": False,
                    "message": t("error_internal_server"),
                    "error_code": "InternalServerError",
                },
            )
