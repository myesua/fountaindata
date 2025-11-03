import asyncio
from typing import Dict, Optional

# NOTE: In a real enterprise system, these keys would be hashed 
# and stored in a database (e.g., PostgreSQL or Vault).
# This mock implements the necessary async lookup for high performance.

API_KEY_STORE: Dict[str, str] = {
    "PREMIUM_KEY_12345": "internal_data_platform", 
    "PARTNER_KEY_67890": "partner_xyz",
}

async def get_client_id_by_api_key(api_key: str) -> Optional[str]:
    """
    Asynchronously looks up the client ID associated with a given API key.
    
    This function mimics a non-blocking database query to maintain 
    high throughput in the event loop.
    """
    await asyncio.sleep(0.001) 
    
    return API_KEY_STORE.get(api_key)