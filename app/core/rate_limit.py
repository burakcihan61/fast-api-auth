"""Rate limiting configuration using slowapi"""

from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.config import settings


def user_or_ip_key_func(request: Request) -> str:
    """
    Custom key function for rate limiting.
    Uses user ID if authenticated, otherwise client IP.
    """
    # Bypass for testing if special header is present
    if request.headers.get("X-Skip-Rate-Limit") == "test-bypass-secret":
        return "bypass-key"

    # Check if user is in request state (set by authentication middleware or dependency)
    user = getattr(request.state, "user", None)
    if user:
        return f"user:{user.id}"

    # Fallback to IP address
    return get_remote_address(request)


# Initialize Limiter
# Using Redis as storage if available, otherwise in-memory
limiter = Limiter(
    key_func=user_or_ip_key_func,
    enabled=settings.RATE_LIMIT_ENABLED,
    storage_uri=settings.REDIS_URL or "memory://",
)


def get_rate_limit(request: Request) -> str:
    """
    Helper to determine dynamic rate limit based on user status.
    Example usage: @limiter.limit(get_rate_limit)
    """
    user = getattr(request.state, "user", None)
    if user and getattr(user, "is_premium", False):
        return f"{settings.RATE_LIMIT_PER_MINUTE * 2}/minute"
    return f"{settings.RATE_LIMIT_PER_MINUTE}/minute"
