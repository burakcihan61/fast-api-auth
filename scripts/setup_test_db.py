
import asyncio
import asyncpg
from app.core.config import settings

async def setup_test_db():
    """Create the test database if it doesn't exist"""
    # Parse the main database URL to get connection details
    # We connect to 'postgres' database to create the new one
    conn_url = settings.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
    # Replace the database name at the end with 'postgres'
    base_url = "/".join(conn_url.split("/")[:-1]) + "/postgres"
    
    # Target database name
    # We try to get it from TEST_DATABASE_URL or use 'myapp_test'
    test_db_url = settings.TEST_DATABASE_URL or ""
    if test_db_url:
        target_db = test_db_url.split("/")[-1]
    else:
        target_db = "myapp_test"

    print(f"Connecting to {base_url} to create {target_db}...")
    
    try:
        conn = await asyncpg.connect(base_url.replace("postgresql://", "postgresql://"))
        
        # Check if exists
        exists = await conn.fetchval(
            "SELECT 1 FROM pg_database WHERE datname=$1", target_db
        )
        
        if not exists:
            await conn.execute(f'CREATE DATABASE "{target_db}"')
            print(f"Database '{target_db}' created successfully.")
        else:
            print(f"Database '{target_db}' already exists.")
            
        await conn.close()
    except Exception as e:
        print(f"Error creating database: {e}")

if __name__ == "__main__":
    asyncio.run(setup_test_db())
