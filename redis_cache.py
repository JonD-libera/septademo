
import redis
import hashlib
import json
from config import REDIS_HOST, REDIS_PORT

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

def cache_result(key_base: str, data: dict, expire: int = 300):
    key = hashlib.sha256(key_base.encode()).hexdigest()
    r.setex(key, expire, json.dumps(data))
    return key

def get_cached_result(key_base: str):
    key = hashlib.sha256(key_base.encode()).hexdigest()
    result = r.get(key)
    return json.loads(result) if result else None
