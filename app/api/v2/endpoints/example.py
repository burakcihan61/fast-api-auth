from typing import Any

from fastapi import APIRouter

from app.core.i18n import t

router = APIRouter()


@router.get("/")
async def example_v2() -> dict[str, Any]:
    """
    Example endpoint for API v2.
    Demonstrates versioning and localization.
    """
    return {
        "message": t("hello"),
        "sub_message": t("welcome"),
        "version": "v2",
        "status": "operational"
    }
