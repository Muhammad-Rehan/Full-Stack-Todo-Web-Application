from typing import Any, Optional
import redis
from ..config import settings


class CacheService:
    def __init__(self):
        self._redis_client = None
        self._redis_available = None

    def _ensure_connection(self):
        """Lazy initialization of Redis connection"""
        if self._redis_available is not None:
            return  # Already initialized

        try:
            self._redis_client = redis.Redis(
                host=settings.redis_host,
                port=settings.redis_port,
                db=0,
                password=settings.redis_password,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5
            )
            # Test the connection
            self._redis_client.ping()
            self._redis_available = True
        except redis.RedisError as e:
            print(f"Redis connection failed: {e}")
            print("Cache service will operate in fallback mode (no caching)")
            self._redis_client = None
            self._redis_available = False

    def get(self, key: str) -> Optional[str]:
        """Get a value from cache"""
        self._ensure_connection()

        if not self._redis_available or not self._redis_client:
            return None
        try:
            return self._redis_client.get(key)
        except redis.RedisError:
            # If Redis is unavailable, return None
            return None

    def set(self, key: str, value: str, expire: int = 3600) -> bool:
        """Set a value in cache with optional expiration (in seconds)"""
        self._ensure_connection()

        if not self._redis_available or not self._redis_client:
            return False
        try:
            return self._redis_client.setex(key, expire, value)
        except redis.RedisError:
            # If Redis is unavailable, return False
            return False

    def delete(self, key: str) -> bool:
        """Delete a key from cache"""
        self._ensure_connection()

        if not self._redis_available or not self._redis_client:
            return False
        try:
            return bool(self._redis_client.delete(key))
        except redis.RedisError:
            # If Redis is unavailable, return False
            return False

    def exists(self, key: str) -> bool:
        """Check if a key exists in cache"""
        self._ensure_connection()

        if not self._redis_available or not self._redis_client:
            return False
        try:
            return bool(self._redis_client.exists(key))
        except redis.RedisError:
            # If Redis is unavailable, return False
            return False


# Global cache instance
cache_service = CacheService()