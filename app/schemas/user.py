"""User schemas for validation and serialization"""

import re
from datetime import datetime
from typing import Annotated, Optional

from pydantic import EmailStr, Field, field_validator

from app.schemas.base import BaseSchema


class UserBase(BaseSchema):
    """Base user schema with common fields"""

    email: EmailStr = Field(..., description="User email address")
    username: Annotated[
        str,
        Field(
            min_length=3,
            max_length=50,
            pattern=r"^[a-zA-Z0-9_-]+$",
            examples=["john_doe", "alice-123"],
        ),
    ]
    full_name: Optional[str] = Field(None, min_length=1, max_length=100)


class UserCreate(UserBase):
    """Schema for creating a new user"""

    password: Annotated[
        str,
        Field(
            min_length=8,
            max_length=100,
            description="Password must contain uppercase, lowercase, number and special char",
        ),
    ]

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """Validate password meets security requirements"""
        if not re.search(r"[A-Z]", v):
            raise ValueError("En az bir büyük harf içermelidir")
        if not re.search(r"[a-z]", v):
            raise ValueError("En az bir küçük harf içermelidir")
        if not re.search(r"\d", v):
            raise ValueError("En az bir rakam içermelidir")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError("En az bir özel karakter içermelidir")

        # Check for common passwords
        common_passwords = ["password", "12345678", "qwerty"]
        if v.lower() in common_passwords:
            raise ValueError("Çok yaygın bir şifre kullanıyorsunuz")

        return v


class UserUpdate(BaseSchema):
    """Schema for updating user (all fields optional)"""

    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, min_length=1, max_length=100)
    password: Optional[str] = Field(None, min_length=8, max_length=100)


class UserResponse(UserBase):
    """User response schema (without sensitive data)"""

    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: Optional[datetime] = None


class UserLogin(BaseSchema):
    """Schema for user login"""

    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=1)


class TokenResponse(BaseSchema):
    """Token response schema"""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseSchema):
    """Token payload schema"""

    sub: Optional[int] = None
    exp: Optional[int] = None
    type: Optional[str] = None
