import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

RATE_LIMIT_COUNT = 1000  
RATE_LIMIT_PERIOD = 60.0 

RATE_LIMIT_STORE: dict = {}

def get_client_key(request: Request) -> str:
    """Determines the client key (e.g., IP address)."""
    return request.client.host if request.client else "default_client"

class BatchRateLimiterMiddleware(BaseHTTPMiddleware):
    """Middleware that enforces a rate limit based on the total number of records."""
    def __init__(self, app, exempt_routes: list):
        super().__init__(app)
        self.exempt_routes = exempt_routes

    async def dispatch(self, request: Request, call_next):
        if request.url.path in self.exempt_routes or request.url.path.endswith('/validate') == False:
            return await call_next(request)
        try:
            body = await request.json()
            batch_size = len(body.get('data_batch', []))
        except Exception:
            return await call_next(request)
        
        client_key = get_client_key(request)
        current_time = time.time()

        if client_key not in RATE_LIMIT_STORE:
            RATE_LIMIT_STORE[client_key] = {
                'tokens': RATE_LIMIT_COUNT,
                'last_check': current_time
            }

        state = RATE_LIMIT_STORE[client_key]
    
        time_passed = current_time - state['last_check']
        replenish_rate = RATE_LIMIT_COUNT / RATE_LIMIT_PERIOD
        new_tokens = time_passed * replenish_rate
        
        state['tokens'] = min(RATE_LIMIT_COUNT, state['tokens'] + new_tokens)
        state['last_check'] = current_time
        if state['tokens'] >= batch_size:
            state['tokens'] -= batch_size
        else:
            remaining_tokens = int(state['tokens'])
            return JSONResponse(
                status_code=429,
                content={
                    "detail": f"Rate limit exceeded for batch size. Requested {batch_size} records, only {remaining_tokens} tokens remain. Try a smaller batch or wait."
                }
            )
        return await call_next(request)
