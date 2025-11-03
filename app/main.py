import uvicorn
from fastapi import FastAPI
from middleware.rate_limiter import BatchRateLimiterMiddleware
from routers.contracts import router as contracts_router
from routers.validation import router as validation_router
from routers.metrics import router as metrics_router
from middleware.metrics_middleware import PrometheusMiddleware
from database.in_memory_registry import CONTRACT_REGISTRY 
from database.db_connector import connect_db, disconnect_db, get_pool
from database.registry import initialize_contracts
from metrics.metrics import DB_CONNECTIONS 


app = FastAPI(
    title="FountainData API: Flow Control",
    description="High-performance data validation and adaptive schema enforcement service.",
    version="3.0.0"
)

# --- GLOBAL MIDDLEWARE ---
app.add_middleware(PrometheusMiddleware)

EXEMPT_PATHS = [
    "/", 
    "/v1/contracts", 
    "/docs", 
    "/openapi.json",
    "/metrics"
]
contracts_paths = [f"/v1/contracts/{k}" for k in CONTRACT_REGISTRY.keys()]
EXEMPT_PATHS.extend(contracts_paths)

app.add_middleware(
    BatchRateLimiterMiddleware,
    exempt_routes=EXEMPT_PATHS
)
# -------------------------

# --- DB Connection Hooks ---
@app.on_event("startup")
async def startup_db_client():
    await connect_db()
    await initialize_contracts() 

@app.on_event("shutdown")
async def shutdown_db_client():
    await disconnect_db()
# ---------------------------

# Include the modular routers
app.include_router(contracts_router)
app.include_router(validation_router)
app.include_router(metrics_router)


@app.get("/", summary="API Status Check")
async def root():
    pool = get_pool()
    if pool:
        DB_CONNECTIONS.set(pool.get_size())
    
    return {
        "message": "FountainData API is running.",
        "status": "OK",
        "endpoints": {
            "documentation": "/docs",
            "validation_example": "/v1/data/cust_events_stream/validate",
            "registry_status": "/v1/contracts/cust_events_stream"
        }
    }

print(f"--- FountaintData API Loaded (v3.0.0) ---")
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)