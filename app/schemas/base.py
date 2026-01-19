"""Base schemas for common response patterns"""

from datetime import datetime
from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel, ConfigDict

DataType = TypeVar("DataType")


class BaseSchema(BaseModel):
    """Base schema with common configuration"""

    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )


class ResponseBase(BaseModel):
    """Base response schema"""

    success: bool = True
    message: Optional[str] = None


class DataResponse(ResponseBase, Generic[DataType]):
    """Generic response schema with data"""

    data: Optional[DataType] = None


class PaginatedResponse(ResponseBase, Generic[DataType]):
    """Paginated response schema"""

    data: list[DataType]
    total: int
    page: int
    page_size: int
    total_pages: int


class ErrorResponse(ResponseBase):
    """Error response schema"""

    success: bool = False
    error_code: Optional[str] = None
    details: Optional[dict[str, Any]] = None
