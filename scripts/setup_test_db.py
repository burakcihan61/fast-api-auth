
import asyncio
from sqlalchemy import text
from app.core.database import engine

async def create_test_db():
    # Connect to the default database to create the new one
    # Note: asyncpg doesn't support 'CREATE DATABASE' easily within a transaction
    # and we need to connect to a different database first.
    
    # We'll use a synchronous connection for this utility if possible,
    # or just try to run it via textual SQL if the engine's DB exists.
    
    # Since we are using asyncpg, we'll try to use the engine to connect to 'postgres' DB
    # instead of 'myapp_db' to create 'myapp_test'.
    
    from sqlalchemy.ext.asyncio import create_async_engine
    import os
    
    base_url = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/myapp_db")
    # Replace DB name with 'postgres'
    postgres_url = base_url.rsplit('/', 1)[0] + '/postgres'
    
    temp_engine = create_async_engine(postgres_url, isolation_level="AUTOCOMMIT")
    
    async with temp_engine.connect() as conn:
        try:
            await conn.execute(text("CREATE DATABASE myapp_test"))
            print("Database 'myapp_test' created successfully.")
        except Exception as e:
            if "already exists" in str(e):
                print("Database 'myapp_test' already exists.")
            else:
                print(f"Error creating database: {e}")
    
    await temp_engine.dispose()

if __name__ == "__main__":
    asyncio.run(create_test_db())
