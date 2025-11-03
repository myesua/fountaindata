from fastapi import APIRouter, HTTPException, status
from database import registry
from schemas.contract_schema import ContractInput

router = APIRouter(
    prefix="/v1/contracts",
    tags=["Contract Registry"],
)

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Register New Data Contract"
)
async def register_new_contract(contract_input: ContractInput):
    source_id = contract_input.source_id
    contract_data = contract_input.model_dump(by_alias=True)
    
    existing_contract = await registry.get_contract_by_source_id(source_id)
    if existing_contract:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Source ID '{source_id}' already has a contract."
        )

    await registry.register_contract(source_id, contract_data)
    return {"message": f"Contract '{contract_input.contract_id}' registered for Source '{source_id}'."}

@router.get("/{source_id}", summary="Get Active Contract by Source ID")
async def get_contract(source_id: str):
    contract = await registry.get_contract_by_source_id(source_id)
    
    if not contract:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contract not found for source_id: {source_id}")
        
    return contract