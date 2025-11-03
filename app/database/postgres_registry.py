import json
from typing import Dict, Any, Optional
from database.db_connector import get_pool
from database.in_memory_registry import CONTRACT_REGISTRY

async def get_contract_by_source_id(source_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves the active contract data for a given source ID from PostgreSQL."""
    pool = get_pool()
    if not pool:
        print("[POSTGRES_REGISTRY] DB Pool not available. Cannot fetch contract.")
        return None
        
    query = "SELECT source_id, contract_id, schema FROM contracts WHERE source_id = $1;"
    
    async with pool.acquire() as connection:
        record = await connection.fetchrow(query, source_id)
        
    if record:
        return {
            "source_id": record['source_id'],
            "contract_id": record['contract_id'],
            "schema": record['schema']
        }
    return None

async def register_contract(source_id: str, contract_data: Dict[str, Any]) -> None:
    """Saves or updates a contract to the registry (UPSERT)."""
    pool = get_pool()
    if not pool:
        raise ConnectionError("Database connection not available for registration.")

    query = """
    INSERT INTO contracts (source_id, contract_id, schema)
    VALUES ($1, $2, $3::jsonb)
    ON CONFLICT (source_id) DO UPDATE SET
        contract_id = EXCLUDED.contract_id,
        schema = EXCLUDED.schema,
        updated_at = NOW();
    """
    schema_json = json.dumps(contract_data['schema'])
    
    async with pool.acquire() as connection:
        await connection.execute(query, source_id, contract_data['contract_id'], schema_json)

async def update_contract(source_id: str, new_contract_data: Dict[str, Any]) -> None:
    """Updates an existing contract (re-uses register_contract logic)."""
    await register_contract(source_id, new_contract_data)

async def initialize_contracts() -> None:
    """
    Inserts initial mock data into the fresh PostgreSQL table if the table is empty.
    """
    pool = get_pool()
    if not pool:
        print("[POSTGRES_REGISTRY] Initialization skipped: DB Pool not available.")
        return

    async with pool.acquire() as connection:
        count = await connection.fetchval("SELECT COUNT(*) FROM contracts;")
        
        if count == 0:
            print("[POSTGRES_REGISTRY] Populating PostgreSQL with initial contract data.")
            for source_id, contract in CONTRACT_REGISTRY.items():
                await register_contract(source_id, contract)
            print("[POSTGRES_REGISTRY] Initial contract data populated.")