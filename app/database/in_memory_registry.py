import asyncio
from typing import Dict, Any, Optional

CONTRACT_REGISTRY: Dict[str, Dict[str, Any]] = {
    "cust_events_stream": {
        "source_id": "cust_events_stream",
        "contract_id": "cust_events_v2",
        "schema": {
            "type": "object",
            "properties": {
                "user_id": {"type": "integer"},
                "event_name": {"type": "string"},
                "timestamp": {"type": "string", "format": "date-time"},
                "product_id": {"type": "string"},
                "price": {"type": "number"}
            },
            "required": ["user_id", "event_name", "timestamp", "price"]
        }
    }
}
