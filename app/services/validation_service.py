import time
import uuid
from typing import List, Dict, Any
from schemas.contract_schema import ValidationResponse, BatchMetrics, InvalidDataMetrics
from services import data_router
from database import registry
from validation import core as validation_core
from validation.risk_assessment import assess_risk
from metrics.metrics import VALIDATION_LATENCY, ADAPTIVE_SCHEMA_COUNT

async def execute_validation(source_id: str, data_batch: List[Dict[str, Any]]) -> ValidationResponse:
    start_time = time.perf_counter()
    
    contract = await registry.get_contract_by_source_id(source_id)
    if not contract:
        raise ValueError(f"Contract not found for source_id: {source_id}")

    validated_model = validation_core.get_pydantic_model(contract)
    valid_data = []
    invalid_data_records = []
    trace_id = str(uuid.uuid4())

    for index, record in enumerate(data_batch):
        result, errors = validation_core.validate_record(validated_model, record)
        if result:
            valid_data.append(result.model_dump(exclude_none=True))
        else:
            invalid_data_records.append({
                "index_in_batch": index,
                "data_payload": record,
                "validation_errors": errors
            })

    # Asynchronously route data
    quarantined_payloads = [item['data_payload'] for item in invalid_data_records]
    await data_router.route_data(source_id, valid_data, quarantined_payloads)

    total = len(data_batch)
    valid_count = len(valid_data)
    invalid_count = len(invalid_data_records)
    
    status = "success" if invalid_count == 0 else ("partial_success" if valid_count > 0 else "failure")

    end_time = time.perf_counter()
    VALIDATION_LATENCY.labels(source_id=source_id).observe(end_time - start_time)

    return ValidationResponse(
        source_id=source_id,
        contract_id=contract['contract_id'],
        trace_id=trace_id,
        status=status,
        batch_metrics=BatchMetrics(
            total_records=total,
            valid_records=valid_count,
            invalid_records=invalid_count
        ),
        valid_data=valid_data,
        invalid_data=InvalidDataMetrics(
            quarantine_id=f"QUARANTINE-{trace_id}",
            records=invalid_data_records
        )
    )


async def execute_adaptation(source_id: str, contract_data: Dict[str, Any]) -> Dict[str, str]:
    existing_contract = await registry.get_contract_by_source_id(source_id)
    if not existing_contract:
        raise ValueError(f"Contract not found for source_id: {source_id}")
        
    new_schema = contract_data['schema']
    risk_status, message = assess_risk(existing_contract['schema'], new_schema)

    if risk_status == "rejected":
        ADAPTIVE_SCHEMA_COUNT.labels(source_id=source_id, result='rejected').inc()
        return {"status": "rejected", "message": message}
    
    await registry.update_contract(source_id, contract_data)
    
    ADAPTIVE_SCHEMA_COUNT.labels(source_id=source_id, result='auto_approved').inc()
    return {"status": "accepted_auto_approved", "message": message}