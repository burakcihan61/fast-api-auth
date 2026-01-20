import asyncio

from sqlalchemy import text

from app.core.database import AsyncSessionLocal


async def t():
    async with AsyncSessionLocal() as db:
        res = await db.execute(
            text(
                "SELECT enumlabel FROM pg_enum JOIN pg_type ON pg_type.oid = pg_enum.enumtypid WHERE pg_type.typname = 'userrole'"
            )
        )
        print(f"Enum labels: {res.all()}")


if __name__ == "__main__":
    asyncio.run(t())
