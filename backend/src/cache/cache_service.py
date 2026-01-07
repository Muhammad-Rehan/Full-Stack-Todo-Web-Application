from typing import Any, Optional
import redis
from ..config import settings


class CacheService:
    def __init__(self):
        try:
            self.redis_client = redis.Redis(
                host=settings.redis_host,
                port=settings.redis_port,
                db=0,
                password=settings.redis_password,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5
            )
            # Test the connection
            self.redis_client.ping()
            self._redis_available = True
        except redis.RedisError as e:
            print(f"Redis connection failed: {e}")
            print("Cache service will operate in fallback mode (no caching)")
            self.redis_client = None
            self._redis_available = False

    def get(self, key: str) -> Optional[str]:
        """Get a value from cache"""
        if not self._redis_available or not self.redis_client:
            return None
        try:
            return self.redis_client.get(key)
        except redis.RedisError:
            # If Redis is unavailable, return None
            return None

    def set(self, key: str, value: str, expire: int = 3600) -> bool:
        """Set a value in cache with optional expiration (in seconds)"""
        if not self._redis_available or not self.redis_client:
            return False
        try:
            return self.redis_client.setex(key, expire, value)
        except redis.RedisError:
            # If Redis is unavailable, return False
            return False

    def delete(self, key: str) -> bool:
        """Delete a key from cache"""
        if not self._redis_available or not self.redis_client:
            return False
        try:
            return bool(self.redis_client.delete(key))
        except redis.RedisError:
            # If Redis is unavailable, return False
            return False

    def exists(self, key: str) -> bool:
        """Check if a key exists in cache"""
        if not self._redis_available or not self.redis_client:
            return False
        try:
            return bool(self.redis_client.exists(key))
        except redis.RedisError:
            # If Redis is unavailable, return False
            return False


# Global cache instance
cache_service = CacheService()