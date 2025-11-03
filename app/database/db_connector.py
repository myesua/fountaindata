import asyncpg
from typing import Optional
from config import DATABASE_URL

_pool: Optional[asyncpg.Pool] = None

async def connect_db():
    """Initializes the asynchronous PostgreSQL connection pool."""
    global _pool
    
    if "fountain_db_default" in DATABASE_URL:
        print("[DB WARNING] Using default localhost DATABASE_URL. Ensure you set the DATABASE_URL environment variable.")

    try:
        print(f"[DB] Attempting to connect to PostgreSQL...")
        _pool = await asyncpg.create_pool(
            dsn=DATABASE_URL,
            min_size=5,       
            max_size=20,      
            timeout=5,        
        )
        print("[DB] PostgreSQL connection pool created successfully.")
        
        # Ensure tables exist 
        await _create_schema()
        
    except Exception as e:
        print(f"[DB ERROR] Could not connect to PostgreSQL: {e}")
        _pool = None 

async def disconnect_db():
    """Closes the connection pool."""
    if _pool:
        print("[DB] Closing PostgreSQL connection pool.")
        await _pool.close()

def get_pool() -> Optional[asyncpg.Pool]:
    """Returns the global connection pool instance."""
    return _pool

async def _create_schema():
    """
    Creates the necessary table if it does not exist.
    """
    if not _pool:
        return
        
    CREATE_TABLE_QUERY = """
    CREATE TABLE IF NOT EXISTS contracts (
        source_id VARCHAR(255) PRIMARY KEY,
        contract_id VARCHAR(255) NOT NULL,
        schema JSONB NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    """
    async with _pool.acquire() as connection:
        await connection.execute(CREATE_TABLE_QUERY)
    print("[DB] Verified 'contracts' table schema.")