"""Create a superuser for the application"""

import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal
from app.crud.user import user as user_crud
from app.schemas.user import UserCreate


async def create_superuser(
    email: str,
    username: str,
    password: str,
    full_name: str = "Admin User",
) -> None:
    """Create a superuser"""
    async with AsyncSessionLocal() as db:
        # Check if user already exists
        existing_user = await user_crud.get_by_email(db, email=email)
        if existing_user:
            print(f"❌ User with email {email} already exists!")
            return

        existing_username = await user_crud.get_by_username(db, username=username)
        if existing_username:
            print(f"❌ User with username {username} already exists!")
            return

        # Create user
        user_in = UserCreate(
            email=email,
            username=username,
            password=password,
            full_name=full_name,
        )
        user = await user_crud.create(db, obj_in=user_in)

        # Make superuser
        user.is_superuser = True
        db.add(user)
        await db.commit()
        await db.refresh(user)

        print(f"✅ Superuser created successfully!")
        print(f"   Email: {user.email}")
        print(f"   Username: {user.username}")
        print(f"   ID: {user.id}")


async def main() -> None:
    """Main function"""
    print("Creating superuser...")

    # You can modify these or take from input
    await create_superuser(
        email="admin@example.com",
        username="admin",
        password="Admin123!@#",
        full_name="System Administrator",
    )


if __name__ == "__main__":
    asyncio.run(main())
