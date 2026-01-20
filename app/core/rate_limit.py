"""Rate limiting configuration using slowapi"""

from contextvars import ContextVar

from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.config import settings
from app.core.security import verify_token

# Global context for the current request
request_var: ContextVar[Request | None] = ContextVar("request", default=None)

def user_or_ip_key_func(request: Request) -> str:
    """
    Custom key function for rate limiting.
    Uses user ID if authenticated, otherwise client IP.
    """
    # Bypass for testing if special header is present
    if request.headers.get("X-Skip-Rate-Limit") == "test-bypass-secret":
        import uuid
        return f"bypass-{uuid.uuid4()}"

    # Try to get user from token in header
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.replace("Bearer ", "")
        payload = verify_token(token)
        if payload and "sub" in payload:
            return f"user:{payload['sub']}"

    # Fallback to IP address
    addr = get_remote_address(request)
    return addr or "127.0.0.1"

# Initialize Limiter
# Using Redis as storage if available, otherwise in-memory
limiter = Limiter(
    key_func=user_or_ip_key_func,
    enabled=settings.RATE_LIMIT_ENABLED,
    headers_enabled=True,
    storage_uri=settings.REDIS_URL or "memory://",
)

def get_dynamic_rate_limit() -> str:
    """
    Helper to determine dynamic rate limit based on user status.
    Uses context variable to access current request.
    Decodes token from Authorization header if present.
    """
    request = request_var.get()

    if request:
        # Try to get is_premium status from token claims
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.replace("Bearer ", "")
            payload = verify_token(token)
            if payload and payload.get("is_premium") is True:
                return f"{settings.RATE_LIMIT_PER_MINUTE * 2}/minute"

    return f"{settings.RATE_LIMIT_PER_MINUTE}/minute"
