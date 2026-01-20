"""FastAPI main application"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.api.v1.router import api_router
from app.core.cache import close_redis, get_redis
from app.core.config import settings
from app.core.database import close_db, init_db
from app.core.logging import logger, setup_logging
from app.core.rate_limit import limiter, request_var
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
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

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

# Rate Limiter Middleware
app.add_middleware(SlowAPIMiddleware)

# Logging Middleware (request/response tracking)
app.add_middleware(LoggingMiddleware)

@app.middleware("http")
async def set_request_context(request: Request, call_next):
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
