"""FastAPI main application"""

from collections.abc import AsyncGenerator, Awaitable, Callable
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.api.v1.router import api_router
from app.api.v2.router import api_router as api_router_v2
from app.core.cache import close_redis, get_redis
from app.core.config import settings
from app.core.database import close_db, init_db
from app.core.logging import logger, setup_logging
from app.core.rate_limit import limiter, request_var
from app.core.i18n import I18nMiddleware
from app.middleware.error_handler import ExceptionHandlerMiddleware
from app.middleware.logging import LoggingMiddleware

# Initialize logging
setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan events"""
    # Startup
    logger.info("Application starting up...")
    await init_db()
    await get_redis()  # Initialize Redis connection
    logger.info("Application startup complete")
    yield
    # Shutdown
    logger.info("Application shutting down...")
    await close_db()
    await close_redis()
    logger.info("Application shutdown complete")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Professional FastAPI Application",
    debug=settings.DEBUG,
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# Rate Limiter state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore

# ==========================================
# Middleware Configuration
# ==========================================


# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)

# Trusted Host Middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.get_allowed_hosts(),
)

# Custom Exception Handler
app.add_middleware(ExceptionHandlerMiddleware)


# Global Exception Handlers (Standardizing errors)
from starlette.exceptions import HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.core.i18n import t

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": t(str(exc.detail)),
            "error_code": "HTTPException",
        },
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": t("validation_error"),
            "details": exc.errors(),
            "error_code": "RequestValidationError",
        },
    )

# Rate Limiter Middleware
app.add_middleware(SlowAPIMiddleware)

# Internationalization Middleware
app.add_middleware(I18nMiddleware)

# Logging Middleware (request/response tracking)
app.add_middleware(LoggingMiddleware)


@app.middleware("http")
async def set_request_context(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    token = request_var.set(request)
    try:
        response = await call_next(request)
    finally:
        request_var.reset(token)
    return response


# ==========================================
# Prometheus Metrics
# ==========================================
# Enable metrics in all environments (for development testing, set to production only in prod)
Instrumentator().instrument(app).expose(app)

# ==========================================
# API Routes
# ==========================================
app.include_router(api_router, prefix="/api/v1")
app.include_router(api_router_v2, prefix="/api/v2")


# ==========================================
# Health Check Endpoints
# ==========================================
@app.get("/health", tags=["health"])
async def health_check() -> dict[str, Any]:
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
    }


@app.get("/", tags=["root"])
async def root() -> dict[str, Any]:
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "redoc": "/redoc",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower(),
    )
