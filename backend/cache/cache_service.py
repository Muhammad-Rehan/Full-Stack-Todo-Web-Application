import redis
import os

class CacheService:
    def __init__(self):
        self.redis = None
        if os.environ.get("REDIS_URL"):
            self.redis = redis.from_url(os.environ["REDIS_URL"])

    def get(self, key):
        if self.redis:
            return self.redis.get(key)
        return None

    def set(self, key, value, expire=None):
        if self.redis:
            return self.redis.set(key, value, ex=expire)
        return None

    def delete(self, key):
        if self.redis:
            return self.redis.delete(key)
        return None

cache_service = CacheService()
