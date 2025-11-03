import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp
from metrics.metrics import REQUEST_COUNT, REQUEST_LATENCY

class PrometheusMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = time.time()
        path = request.scope.get('route').path if request.scope.get('route') else 'unrouted'
        method = request.method

        try:
            response = await call_next(request)
            status_code = response.status_code
            
        except Exception:
            status_code = 500
            raise
        finally:
            request_duration = time.time() - start_time
            
            REQUEST_LATENCY.labels(method=method, endpoint=path).observe(request_duration)
            REQUEST_COUNT.labels(method=method, endpoint=path, status_code=status_code).inc()

        return response