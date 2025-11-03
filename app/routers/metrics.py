from fastapi import APIRouter
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response

router = APIRouter(
    tags=["Monitoring"],
)

@router.get("/metrics", summary="Prometheus Metrics Endpoint")
async def metrics_endpoint():
    data = generate_latest()
    
    return Response(
        content=data, 
        media_type=CONTENT_TYPE_LATEST
    )