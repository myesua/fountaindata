from prometheus_client import Counter, Histogram, Gauge

REQUEST_COUNT = Counter(
    'http_requests_total', 
    'Total count of HTTP requests served', 
    ['method', 'endpoint', 'status_code']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds', 
    'Histogram of HTTP request duration', 
    ['method', 'endpoint'],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0)
)

DB_CONNECTIONS = Gauge(
    'db_pool_current_connections', 
    'Current number of connections in the PostgreSQL pool'
)

RECORDS_PROCESSED_TOTAL = Counter(
    'data_records_processed_total', 
    'Total data records processed by the validation service', 
    ['source_id', 'status']
)

VALIDATION_LATENCY = Histogram(
    'data_validation_duration_seconds', 
    'Latency of the core schema validation function', 
    ['source_id'],
    buckets=(0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5) 
)

ADAPTIVE_SCHEMA_COUNT = Counter(
    'adaptive_schema_changes_total',
    'Total contract adaptation attempts',
    ['source_id', 'result']
)