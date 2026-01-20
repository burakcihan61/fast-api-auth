"""Redis cache utilities"""

import json
from collections.abc import Callable
from functools import wraps
from typing import Any, cast

import redis.asyncio as redis

from app.core.config import settings

# Redis client instance
redis_client: redis.Redis | None = None


async def get_redis() -> redis.Redis:
    """Get Redis client instance"""
    global redis_client
    if redis_client is None:
        redis_client = await redis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
        )
    return redis_client


async def close_redis() -> None:
    """Close Redis connection"""
    global redis_client
    if redis_client:
        await redis_client.close()
        redis_client = None


def cache_result(expire: int = 300, key_prefix: str = "") -> Callable:
    """
    Cache decorator for async functions

    Args:
        expire: Cache expiration time in seconds (default: 300)
        key_prefix: Prefix for cache key (default: function name)

    Example:
        @cache_result(expire=600, key_prefix="popular_posts")
        async def get_popular_posts():
            # Expensive database query
            return posts
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            client = await get_redis()

            # Create cache key
            prefix = key_prefix or func.__name__
            cache_key = f"{prefix}:{args}:{kwargs}"

            # Try to get from cache
            cached = await client.get(cache_key)
            if cached:
                return json.loads(cached)

            # Execute function and cache result
            result = await func(*args, **kwargs)
            await client.setex(cache_key, expire, json.dumps(result, default=str))
            return result

        return wrapper

    return decorator


async def invalidate_cache(pattern: str) -> int:
    """
    Invalidate cache entries matching pattern

    Args:
        pattern: Redis key pattern (e.g., "user:*")

    Returns:
        Number of keys deleted
    """
    client = await get_redis()
    keys = await client.keys(pattern)
    if keys:
        return cast(int, await client.delete(*keys))
    return 0


# ==========================================
# Token Blacklist Functions
# ==========================================


async def blacklist_token(token: str, expire_seconds: int = 1800) -> bool:
    """
    Add token to blacklist (for logout)

    Args:
        token: JWT token to blacklist
        expire_seconds: TTL for blacklist entry (default: 30 min)

    Returns:
        True if successful, False otherwise
    """
    try:
        print("[DEBUG] Attempting to blacklist token...")
        client = await get_redis()
        print(f"[DEBUG] Redis client obtained: {type(client)}")
        if client:
            key = f"blacklist:{token}"
            print(f"[DEBUG] Setting key: {key}")
            await client.set(key, "1", ex=expire_seconds)
            print("[DEBUG] Token blacklisted successfully")
            return True
        print("[DEBUG] Redis client is None!")
        return False
    except Exception as e:
        import traceback

        print(f"[ERROR] Error blacklisting token: {e}")
        print(f"[ERROR] Traceback: {traceback.format_exc()}")
        return False


async def is_token_blacklisted(token: str) -> bool:
    """
    Check if token is blacklisted

    Args:
        token: JWT token to check

    Returns:
        True if blacklisted, False otherwise
    """
    try:
        client = await get_redis()
        if client:
            key = f"blacklist:{token}"
            result = await client.get(key)
            return result is not None
        return False
    except Exception as e:
        print(f"Error checking blacklist: {e}")
        return False


async def remove_from_blacklist(token: str) -> bool:
    """
    Remove token from blacklist (admin function)

    Args:
        token: JWT token to remove from blacklist

    Returns:
        True if successful, False otherwise
    """
    try:
        client = await get_redis()
        if client:
            key = f"blacklist:{token}"
            await client.delete(key)
            return True
        return False
    except Exception as e:
        print(f"Error removing from blacklist: {e}")
        return False
