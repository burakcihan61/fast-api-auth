"""Worker entry point"""

from app.core.logging import logger

# This file is used to start the celery worker:
# celery -A app.worker worker --loglevel=info

logger.info("Celery worker entry point loaded")
