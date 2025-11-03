from typing import Optional
from fastapi import Header, HTTPException
from database.api_key_registry import get_client_id_by_api_key

async def api_key_auth(
    x_api_key: Optional[str] = Header(None, description="The secret API key required for data flow endpoints.")
) -> str:
    if not x_api_key:
        raise HTTPException(
            status_code=401, 
            detail="API Key required: Please provide 'X-API-Key' header."
        )

    client_id = await get_client_id_by_api_key(x_api_key)
    
    if client_id is None:
        raise HTTPException(
            status_code=401, 
            detail="Invalid API Key provided. Access denied."
        )
        
    return client_id