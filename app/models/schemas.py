from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class ContractSchema(BaseModel):
    """The JSON Schema that defines the data structure."""
    type: str = Field(..., description="Must be 'object' for data records.")
    properties: Dict[str, Dict[str, Any]]
    required: List[str] = Field(default_factory=list)

class ContractInput(BaseModel):
    """Input model for registering a new contract."""
    source_id: str = Field(..., description="Unique identifier for the data source (Fountain).")
    contract_id: str = Field(..., description="Version identifier for the contract, e.g., 'cust_events_v2'.")
    schema_definition: ContractSchema = Field(..., alias="schema")

class ValidationRequest(BaseModel):
    """Input model for the /validate endpoint."""
    data_batch: List[Dict[str, Any]]

class ValidationErrorDetail(BaseModel):
    """Details for a single validation error on a field."""
    field: str
    type: str
    message: str

class InvalidRecord(BaseModel):
    """An individual record that failed validation."""
    index_in_batch: int
    data_payload: Dict[str, Any]
    validation_errors: List[ValidationErrorDetail]

class InvalidDataContainer(BaseModel):
    """Container for all invalid records, designed for quarantine."""
    quarantine_id: str
    records: List[InvalidRecord]

class BatchMetrics(BaseModel):
    """Summary metrics for the validation job."""
    total_records: int
    valid_records: int
    invalid_records: int

class ValidationResponse(BaseModel):
    """The final response structure for the /validate endpoint."""
    source_id: str
    contract_id: str
    trace_id: str
    status: str
    batch_metrics: BatchMetrics
    valid_data: List[Dict[str, Any]]
    invalid_data: Optional[InvalidDataContainer] = None
