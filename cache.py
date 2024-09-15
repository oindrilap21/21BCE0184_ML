import redis

r = redis.Redis(host='localhost', port=6379, db=0)

def get_from_cache(key: str):
    return r.get(key)

def set_to_cache(key: str, value, expiration=3600):
    r.set(key, value, ex=expiration)
