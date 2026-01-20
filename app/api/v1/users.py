"""User management endpoints"""

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import RoleChecker, get_current_active_user, get_current_superuser
from app.core.database import get_db
from app.core.rate_limit import get_dynamic_rate_limit, limiter
from app.crud.user import user as user_crud
from app.models.user import User, UserRole
from app.schemas.base import DataResponse, PaginatedResponse
from app.schemas.user import UserResponse, UserUpdate

router = APIRouter()


@router.get("/me", response_model=DataResponse[UserResponse])
@limiter.limit(get_dynamic_rate_limit)
async def get_current_user_info(
    request: Request,
    response: Response,
    current_user: User = Depends(get_current_active_user),
) -> DataResponse[UserResponse]:
    """Get current user information"""
    return JSONResponse(
        content=jsonable_encoder(
            DataResponse(
                success=True,
                message="User retrieved successfully",
                data=UserResponse.model_validate(current_user),
            )
        )
    )


@router.put("/me", response_model=DataResponse[UserResponse])
async def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> DataResponse[UserResponse]:
    """Update current user information"""
    updated_user = await user_crud.update(db, db_obj=current_user, obj_in=user_update)
    await db.commit()
    await db.refresh(updated_user)

    return DataResponse(
        success=True,
        message="User updated successfully",
        data=UserResponse.model_validate(updated_user),
    )


@router.get("", response_model=PaginatedResponse[UserResponse])
async def get_users(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    current_user: User = Depends(RoleChecker([UserRole.ADMIN, UserRole.MODERATOR])),
    db: AsyncSession = Depends(get_db),
) -> PaginatedResponse[UserResponse]:
    """
    Get all users (superuser only)

    Supports pagination via skip and limit parameters.
    """
    users = await user_crud.get_multi(db, skip=skip, limit=limit)
    total = await user_crud.count(db)

    return PaginatedResponse(
        success=True,
        message="Users retrieved successfully",
        data=[UserResponse.model_validate(user) for user in users],
        total=total,
        page=skip // limit + 1 if limit > 0 else 1,
        page_size=limit,
        total_pages=(total + limit - 1) // limit if limit > 0 else 1,
    )


@router.get("/{user_id}", response_model=DataResponse[UserResponse])
async def get_user(
    user_id: int,
    current_user: User = Depends(get_current_superuser),
    db: AsyncSession = Depends(get_db),
) -> DataResponse[UserResponse]:
    """Get user by ID (superuser only)"""
    user = await user_crud.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return DataResponse(
        success=True,
        message="User retrieved successfully",
        data=UserResponse.model_validate(user),
    )


@router.delete("/{user_id}", response_model=DataResponse[UserResponse])
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_superuser),
    db: AsyncSession = Depends(get_db),
) -> DataResponse[UserResponse]:
    """Delete user (superuser only)"""
    user = await user_crud.delete(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    await db.commit()

    return DataResponse(
        success=True,
        message="User deleted successfully",
        data=UserResponse.model_validate(user),
    )
