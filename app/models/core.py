from typing import Dict, Any, Type, List, Optional
from pydantic import BaseModel, create_model

def create_pydantic_model_from_json(model_name: str, json_schema: Dict[str, Any]) -> Type[BaseModel]:
    """
    Dynamically creates a Pydantic model from a JSON Schema.

    This is the core performance driver: it compiles the schema into native
    Python code for extremely fast validation.
    """
    fields: Dict[str, Any] = {}
    required_fields: List[str] = json_schema.get('required', [])
    
    TYPE_MAP = {
        "string": str,
        "integer": int,
        "number": float,
        "boolean": bool,
        "array": List,
        "object": Dict,
    }

    properties: Dict[str, Any] = json_schema.get('properties', {})

    for name, definition in properties.items():
        json_type_str = definition.get('type')
        python_type = TYPE_MAP.get(json_type_str, object) 

        if name in required_fields:
            fields[name] = (python_type, ...) 
        else:
            fields[name] = (Optional[python_type], None)
    return create_model(model_name, **fields)
