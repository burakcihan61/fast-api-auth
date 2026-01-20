"""Base schemas for common response patterns"""

from typing import Any, Generic, TypeVar

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
    message: str | None = None


class DataResponse(ResponseBase, Generic[DataType]):
    """Generic response schema with data"""

    data: DataType | None = None


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
    error_code: str | None = None
    details: dict[str, Any] | None = None
