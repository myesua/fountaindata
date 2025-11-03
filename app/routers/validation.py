from fastapi import APIRouter, HTTPException, Path, Depends
from schemas.contract_schema import ValidationRequest, ValidationResponse, ContractInput
from services import validation_service as service
from middleware.api_key_auth import api_key_auth

router = APIRouter(
    prefix="/v1/data",
    tags=["Data Flow Control"],
)

@router.post(
    "/{source_id}/validate", 
    response_model=ValidationResponse, 
    status_code=200, 
    summary="Real-time Data Validation"
)
async def validate_data(
    request: ValidationRequest,
    source_id: str = Path(...),
    client_id: str = Depends(api_key_auth) 
):
    print(f"Validation Request from Client ID: {client_id}") 
    
    try:
        response = await service.execute_validation(source_id, request.data_batch)
        return response
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error during validation: {e}")


@router.post("/{source_id}/adapt", summary="Adaptive Schema Change Request")
async def adapt_contract(
    contract_input: ContractInput,
    source_id: str = Path(...),
    client_id: str = Depends(api_key_auth) 
):
    contract_data = contract_input.model_dump(by_alias=True)
    
    try:
        result = await service.execute_adaptation(source_id, contract_data)
        if result['status'] == "rejected":
            raise HTTPException(status_code=403, detail=result['message'])
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"Source ID not found: {source_id}")