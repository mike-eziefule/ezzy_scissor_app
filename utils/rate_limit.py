from functools import wraps
import time
from fastapi import HTTPException, Request, status

def rate_limiter(max_calls: int, time_frame:int):
    """
    max_call: the maximum number of calls allowed
    time_frame: the time frame(in seconds) for whch the limit applies
    """
    
    def decorator(func):
        calls = []
        
        @wraps(func)
        async def wrapper( request:Request, *args, **kwargs):
            now = time.time()
            calls_in_time_frame = [call for call in calls if call > now - time_frame]
            if len(calls_in_time_frame) >= max_calls:
                raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail = "Rate limit exceeded")
            calls.append(now)
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator
                