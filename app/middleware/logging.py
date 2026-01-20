"""Logging middleware for request/response tracking"""

import time
import uuid
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from app.core.logging import access_logger, logger


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for logging HTTP requests and responses
    
    Features:
    - Request/Response logging
    - Correlation ID tracking
    - Performance monitoring
    - Error logging
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Generate correlation ID
        correlation_id = str(uuid.uuid4())
        request.state.correlation_id = correlation_id
        
        # Start time
        start_time = time.time()
        
        # Request info
        request_info = {
            "correlation_id": correlation_id,
            "method": request.method,
            "url": str(request.url),
            "path": request.url.path,
            "client_host": request.client.host if request.client else None,
            "user_agent": request.headers.get("user-agent"),
        }
        
        # Log request
        logger.info(
            f"Request started: {request.method} {request.url.path}",
            extra={"event": "request_started", **request_info},
        )
        
        try:
            # Process request
            response = await call_next(request)
            
            # Calculate duration
            duration = time.time() - start_time
            
            # Response info
            response_info = {
                **request_info,
                "status_code": response.status_code,
                "duration_ms": round(duration * 1000, 2),
            }
            
            # Add correlation ID to response headers
            response.headers["X-Correlation-ID"] = correlation_id
            
            # Log response
            log_level = "info" if response.status_code < 400 else "warning"
            if response.status_code >= 500:
                log_level = "error"
            
            getattr(logger, log_level)(
                f"Request completed: {request.method} {request.url.path} "
                f"- {response.status_code} ({duration:.3f}s)",
                extra={"event": "request_completed", **response_info},
            )
            
            # Access log
            access_logger.info(
                f"{request.method} {request.url.path} {response.status_code} {duration:.3f}s",
                extra=response_info,
            )
            
            return response
            
        except Exception as exc:
            # Calculate duration
            duration = time.time() - start_time
            
            # Log error
            logger.error(
                f"Request failed: {request.method} {request.url.path} - {str(exc)}",
                extra={
                    "event": "request_failed",
                    **request_info,
                    "error": str(exc),
                    "error_type": type(exc).__name__,
                    "duration_ms": round(duration * 1000, 2),
                },
                exc_info=True,
            )
            
            raise


def log_exception(exc: Exception, context: dict = None) -> None:
    """
    Log exception with context
    
    Args:
        exc: Exception instance
        context: Additional context dictionary
    """
    error_info = {
        "error": str(exc),
        "error_type": type(exc).__name__,
        "event": "exception",
    }
    
    if context:
        error_info.update(context)
    
    logger.error(
        f"Exception occurred: {type(exc).__name__}: {str(exc)}",
        extra=error_info,
        exc_info=True,
    )


def log_database_query(query: str, duration: float, params: dict = None) -> None:
    """
    Log database query performance
    
    Args:
        query: SQL query
        duration: Query duration in seconds
        params: Query parameters
    """
    query_info = {
        "event": "database_query",
        "query": query[:200],  # Truncate long queries
        "duration_ms": round(duration * 1000, 2),
    }
    
    if params:
        query_info["params"] = str(params)[:100]
    
    # Warn on slow queries (> 1 second)
    if duration > 1.0:
        logger.warning(
            f"Slow database query ({duration:.3f}s): {query[:100]}...",
            extra=query_info,
        )
    else:
        logger.debug(
            f"Database query executed ({duration:.3f}s)",
            extra=query_info,
        )


def log_cache_operation(
    operation: str,
    key: str,
    hit: bool = None,
    duration: float = None,
) -> None:
    """
    Log cache operations
    
    Args:
        operation: Operation type (get, set, delete)
        key: Cache key
        hit: Cache hit (True/False/None)
        duration: Operation duration in seconds
    """
    cache_info = {
        "event": "cache_operation",
        "operation": operation,
        "key": key,
    }
    
    if hit is not None:
        cache_info["hit"] = hit
    
    if duration:
        cache_info["duration_ms"] = round(duration * 1000, 2)
    
    logger.debug(f"Cache {operation}: {key}", extra=cache_info)


def log_authentication(
    username: str,
    success: bool,
    reason: str = None,
    ip_address: str = None,
) -> None:
    """
    Log authentication attempts
    
    Args:
        username: Username attempting authentication
        success: Whether authentication succeeded
        reason: Failure reason (if applicable)
        ip_address: Client IP address
    """
    auth_info = {
        "event": "authentication",
        "username": username,
        "success": success,
    }
    
    if ip_address:
        auth_info["ip_address"] = ip_address
    
    if success:
        logger.info(
            f"Successful authentication: {username}",
            extra=auth_info,
        )
    else:
        auth_info["reason"] = reason or "unknown"
        logger.warning(
            f"Failed authentication: {username} - {reason}",
            extra=auth_info,
        )
