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

def get_contract_by_source_id(source_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves the active contract data for a given fountain ID."""
    return CONTRACT_REGISTRY.get(source_id)

def register_contract(source_id: str, contract_data: Dict[str, Any]) -> None:
    """Saves a new contract to the registry."""
    CONTRACT_REGISTRY[source_id] = contract_data

def update_contract(source_id: str, new_contract_data: Dict[str, Any]) -> None:
    """Updates an existing contract (used in the adaptive logic)."""
    CONTRACT_REGISTRY[source_id] = new_contract_data
