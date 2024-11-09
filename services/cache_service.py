from redis import Redis
import json

rd = Redis(host='redis', port=6379, db=0)

def get_cache(key: str):
    cache = rd.get(key)
    if cache:
        try:
            return json.loads(cache)
        except json.JSONDecodeError:
            return None
    return None

def set_cache(key: str, data: dict, ttl: int = 86400):
    try:
        rd.set(key, json.dumps(data))
        rd.expire(key, ttl)
    except json.JSONDecodeError:
        pass