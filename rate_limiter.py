
from redis_cache import r
from fastapi import HTTPException
from config import RATE_LIMIT, RATE_WINDOW

# It's proxied so...
def get_real_ip(request: Request):
    xff = request.headers.get("X-Real-IP")
    if xff:
        return xff.split(",")[0].strip()
    return request.client.host

def check_rate_limit(request: Request):
    ip = get_real_ip(request)
    key = f"rate:{ip}"
    current = r.get(key)
    if current is None:
        r.set(key, 1, ex=RATE_WINDOW)
    elif int(current) < RATE_LIMIT:
        r.incr(key)
    else:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
