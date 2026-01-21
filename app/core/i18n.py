import json
from contextlib import asynccontextmanager
from contextvars import ContextVar
from pathlib import Path
from typing import Any

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from app.core.config import settings

# Context variable to store the current language for the request
_language_ctx: ContextVar[str] = ContextVar("language", default=settings.DEFAULT_LANGUAGE)
# Cache for loaded translations
_translations: dict[str, dict[str, str]] = {}


def load_translations() -> None:
    """Load translation files from the locales directory."""
    locales_dir = Path(__file__).parent.parent / "locales"
    for lang in settings.SUPPORTED_LANGUAGES:
        file_path = locales_dir / f"{lang}.json"
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                _translations[lang] = json.load(f)
        else:
            _translations[lang] = {}


def get_language() -> str:
    """Get the current language from context."""
    return _language_ctx.get()


def t(key: str, **kwargs: Any) -> str:
    """
    Translate a key into the current language.
    Supports simple format string substitution.
    """
    lang = get_language()
    # Fallback to default language if current language not loaded
    msg = _translations.get(lang, {}).get(key)
    if msg is None:
        # Fallback to default language
        msg = _translations.get(settings.DEFAULT_LANGUAGE, {}).get(key, key)
    
    if kwargs:
        try:
            return msg.format(**kwargs)
        except Exception:
            return msg
    return msg


class I18nMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        accept_language = request.headers.get("Accept-Language")
        lang = settings.DEFAULT_LANGUAGE
        
        if accept_language:
            # Simple parsing: take the first preferred language
            # Example: "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7" -> "tr"
            parsed_lang = accept_language.split(",")[0].strip().split("-")[0]
            if parsed_lang in settings.SUPPORTED_LANGUAGES:
                lang = parsed_lang
        
        token = _language_ctx.set(lang)
        try:
            response = await call_next(request)
            response.headers["Content-Language"] = lang
            return response
        finally:
            _language_ctx.reset(token)


# Initialize translations on module import (or better, on startup)
load_translations()
