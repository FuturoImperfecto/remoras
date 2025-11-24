"""Redis utilities."""

import redis
from django.conf import settings


def get_redis_client() -> redis.Redis:
    """Get Redis client instance."""
    return redis.from_url(settings.REDIS_URL, decode_responses=True)


class RedisCache:
    """Redis cache wrapper."""

    def __init__(self):
        self.client = get_redis_client()

    def get(self, key: str) -> str | None:
        """Get value from cache."""
        return self.client.get(key)

    def set(self, key: str, value: str, ttl: int = 3600) -> bool:
        """Set value in cache with TTL."""
        return self.client.setex(key, ttl, value)

    def delete(self, key: str) -> bool:
        """Delete key from cache."""
        return bool(self.client.delete(key))

    def exists(self, key: str) -> bool:
        """Check if key exists."""
        return bool(self.client.exists(key))

    def increment(self, key: str, amount: int = 1) -> int:
        """Increment counter."""
        return self.client.incrby(key, amount)

    def decrement(self, key: str, amount: int = 1) -> int:
        """Decrement counter."""
        return self.client.decrby(key, amount)


cache = RedisCache()
