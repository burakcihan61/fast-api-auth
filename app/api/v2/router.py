from fastapi import APIRouter

from app.api.v2.endpoints import example

api_router = APIRouter()

api_router.include_router(example.router, prefix="/example", tags=["example-v2"])
