from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class ValidationRequest(BaseModel):
    data_batch: List[Dict[str, Any]] = Field(..., description="A list of data records to validate.")

class ValidationErrorDetail(BaseModel):
    field: str
    type: str
    message: str

class InvalidRecord(BaseModel):
    index_in_batch: int
    data_payload: Dict[str, Any]
    validation_errors: List[ValidationErrorDetail]

class InvalidDataMetrics(BaseModel):
    quarantine_id: str
    records: List[InvalidRecord]

class BatchMetrics(BaseModel):
    total_records: int
    valid_records: int
    invalid_records: int

class ValidationResponse(BaseModel):
    source_id: str
    contract_id: str
    trace_id: str
    status: str = Field(..., description="success, partial_success, or failure")
    batch_metrics: BatchMetrics
    valid_data: List[Dict[str, Any]]
    invalid_data: InvalidDataMetrics

class ContractInput(BaseModel):
    source_id: str
    contract_id: str
    schema: Dict[str, Any]