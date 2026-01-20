"""Authentication endpoints"""

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import bearer_scheme, oauth2_scheme
from app.core.database import get_db
from app.core.logging import logger
from app.core.rate_limit import limiter
from app.core.security import create_access_token, create_refresh_token
from app.crud.user import user as user_crud
from app.middleware.logging import log_authentication
from app.schemas.base import DataResponse
from app.schemas.user import TokenResponse, UserCreate, UserResponse

router = APIRouter()


@router.post(
    "/register", response_model=DataResponse[UserResponse], status_code=status.HTTP_201_CREATED
)
@limiter.limit("5/minute")
async def register(
    request: Request, response: Response, user_in: UserCreate, db: AsyncSession = Depends(get_db)
) -> DataResponse[UserResponse]:
    """
    Register a new user

    - **email**: Valid email address
    - **username**: Unique username (3-50 characters)
    - **password**: Strong password (min 8 chars with uppercase, lowercase, number, special char)
    """
    # Check if user already exists
    existing_user = await user_crud.get_by_email(db, email=user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    existing_username = await user_crud.get_by_username(db, username=user_in.username)
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken",
        )

    # Create new user
    user = await user_crud.create(db, obj_in=user_in)
    await db.commit()

    # Log successful registration
    logger.info(
        f"New user registered: {user.username}",
        extra={
            "event": "user_registered",
            "user_id": user.id,
            "username": user.username,
        },
    )

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(DataResponse(
        success=True,
        message="User registered successfully",
        data=UserResponse.model_validate(user),
    )))


@router.post("/login", response_model=DataResponse[TokenResponse])
@limiter.limit("10/minute")
async def login(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> DataResponse[TokenResponse]:
    """
    OAuth2 compatible login endpoint

    - **username**: Username
    - **password**: Password
    """
    # Authenticate user
    user = await user_crud.authenticate(
        db, username=form_data.username, password=form_data.password
    )
    if not user:
        # Log failed login
        log_authentication(
            username=form_data.username,
            success=False,
            reason="invalid_credentials",
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )

    # Create tokens (sub must be string for jose library)
    access_token = create_access_token(data={"sub": str(user.id), "is_premium": user.is_premium})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    # Log successful login
    log_authentication(
        username=user.username,
        success=True,
    )

    return JSONResponse(content=jsonable_encoder(DataResponse(
        success=True,
        message="Login successful",
        data=TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
        ),
    )))


@router.post("/logout", response_model=DataResponse[dict])
async def logout(
    oauth_token: str | None = Depends(oauth2_scheme),
    bearer_token: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> DataResponse[dict]:
    """
    Logout endpoint - blacklists the current token

    The token will be invalid after logout and cannot be reused.
    Token remains blacklisted until its natural expiration (30 minutes).
    """
    from app.core.cache import blacklist_token

    # Get token from either source
    token = None
    if bearer_token:
        token = bearer_token.credentials
    elif oauth_token:
        token = oauth_token

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No token provided",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Blacklist the token (TTL = 30 minutes, same as token expiration)
    success = await blacklist_token(token, expire_seconds=1800)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Logout failed. Please try again.",
        )

    return DataResponse(
        success=True,
        message="Logout successful",
        data={"message": "Token has been revoked"},
    )
