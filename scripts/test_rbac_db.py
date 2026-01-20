
import asyncio
from app.core.database import AsyncSessionLocal as SessionLocal
from app.crud.user import user as user_crud
from app.models.user import UserRole, User
from app.schemas.user import UserCreate

async def run_test():
    async with SessionLocal() as db:
        # 1. Test registration with role
        print("Testing registration with ADMIN role...")
        username = "test_admin_auth"
        email = "test_admin@example.com"
        
        # Cleanup if exists
        existing = await user_crud.get_by_username(db, username=username)
        if existing:
            await db.delete(existing)
            await db.commit()
            
        user_in = UserCreate(
            username=username,
            email=email,
            password="Password123!",
            full_name="Test Admin",
            role=UserRole.ADMIN
        )
        new_user = await user_crud.create(db, obj_in=user_in)
        await db.commit()
        await db.refresh(new_user)
        
        print(f"Created user: {new_user.username}, Role in DB: {new_user.role}")
        assert new_user.role == UserRole.ADMIN
        
        # 2. Test fetching with role
        fetched_user = await user_crud.get(db, id=new_user.id)
        print(f"Fetched user: {fetched_user.username}, Role: {fetched_user.role}")
        
        # Cleanup
        await db.delete(fetched_user)
        await db.commit()
        print("Test passed successfully!")

if __name__ == "__main__":
    asyncio.run(run_test())
