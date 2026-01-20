"""API dependencies - reusable dependency injection"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import verify_token
from app.crud.user import user as user_crud
from app.models.user import User, UserRole

# OAuth2 scheme for token authentication (username/password in Swagger)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login", auto_error=False)

# HTTPBearer scheme for manual token input in Swagger
bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    db: AsyncSession = Depends(get_db),
    oauth_token: str | None = Depends(oauth2_scheme),
    bearer_token: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> User:
    """
    Get current authenticated user from JWT token
    Accepts token from either OAuth2 password flow or HTTPBearer (manual token input)

    Raises:
        HTTPException: If token is invalid or user not found
    """
    # Get token from either source
    token = None
    if bearer_token:
        token = bearer_token.credentials
    elif oauth_token:
        token = oauth_token

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if token is blacklisted (logged out)
    from app.core.cache import is_token_blacklisted

    if await is_token_blacklisted(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id_raw = payload.get("sub")
    if user_id_raw is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Convert string to int (jose requires sub to be string)
    try:
        user_id = int(str(user_id_raw))
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from None

    user = await user_crud.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Get current active user

    Raises:
        HTTPException: If user is inactive
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_superuser(current_user: User = Depends(get_current_active_user)) -> User:
    """
    Get current superuser

    Raises:
        HTTPException: If user is not a superuser
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user


class RoleChecker:
    """
    Dependency to check if the current user has any of the required roles.

    Example:
        @router.get("/admin", dependencies=[Depends(RoleChecker([UserRole.ADMIN]))])
        def admin_endpoint():
            ...
    """

    def __init__(self, allowed_roles: list[UserRole]):
        self.allowed_roles = allowed_roles

    async def __call__(
        self,
        current_user: User = Depends(get_current_active_user),
    ) -> User:
        """
        Check if user role is in allowed roles.

        Returns:
            The authenticated user if role is allowed.
        """
        if current_user.is_superuser:
            return current_user

        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{current_user.role}' does not have enough permissions. "
                f"Required: {', '.join([r.value for r in self.allowed_roles])}",
            )
        return current_user
