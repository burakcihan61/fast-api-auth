"""Initialize database with tables and optional seed data"""

import asyncio

from app.core.config import settings
from app.core.database import init_db


async def main() -> None:
    """Initialize database"""
    print(f"Creating database tables for {settings.APP_NAME}...")
    print(f"Database URL: {settings.DATABASE_URL}")

    await init_db()

    print("✅ Database initialized successfully!")


if __name__ == "__main__":
    asyncio.run(main())
