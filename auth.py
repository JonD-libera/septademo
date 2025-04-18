
from redis_cache import r
from fastapi import Request, HTTPException
from config import USE_AUTH

def check_auth(request: Request):
    if not USE_AUTH:
        return
    token = request.headers.get("Authorization")
    if not token or not r.sismember("valid_tokens", token.replace("Bearer ", "")):
        raise HTTPException(status_code=403, detail="Invalid or missing token")
