from typing import Any

from fastapi import APIRouter

router = APIRouter()


@router.get("/example")
async def example_v2() -> dict[str, Any]:
    """
    Example endpoint for API v2.
    Demonstrates versioning.
    """
    return {
        "message": "Hello from API v2!",
        "version": "v2",
        "status": "operational"
    }
