from typing import Dict, Any, Optional, Tuple, List
from pydantic import create_model, BaseModel, ValidationError, Field

MODEL_CACHE: Dict[str, type[BaseModel]] = {}

def get_pydantic_model(contract: Dict[str, Any]) -> type[BaseModel]:
    source_id = contract['source_id']
    if source_id in MODEL_CACHE:
        return MODEL_CACHE[source_id]
    
    schema = contract['schema']
    properties = schema.get('properties', {})
    required_fields = schema.get('required', [])

    # Map JSON Schema properties to Pydantic field definitions
    field_definitions = {}
    for name, prop in properties.items():
        type_hint = Any 
        
        # Simple type mapping for required fields
        if name in required_fields:
            if prop.get('type') == 'integer':
                type_hint = int
            elif prop.get('type') == 'number':
                type_hint = float
            elif prop.get('type') == 'string':
                type_hint = str
            
            field_definitions[name] = (type_hint, Field(..., description=name))
        
        # Simple type mapping for optional fields
        else:
            if prop.get('type') == 'integer':
                type_hint = Optional[int]
            elif prop.get('type') == 'number':
                type_hint = Optional[float]
            elif prop.get('type') == 'string':
                type_hint = Optional[str]
                
            field_definitions[name] = (type_hint, None)

    DynamicModel = create_model(f'{source_id}_Model', **field_definitions)
    MODEL_CACHE[source_id] = DynamicModel
    return DynamicModel

def validate_record(model: type[BaseModel], record: Dict[str, Any]) -> Tuple[Optional[BaseModel], Optional[List[Dict[str, str]]]]:
    try:
        validated_data = model.model_validate(record)
        return validated_data, None
    except ValidationError as e:
        error_details = []
        for error in e.errors():
            field = error['loc'][0] if error['loc'] else 'record'
            error_details.append({
                "field": str(field),
                "type": error['type'],
                "message": error['msg']
            })
        return None, error_details