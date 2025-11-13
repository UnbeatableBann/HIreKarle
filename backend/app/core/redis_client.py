import json
from typing import Optional, Any
from redis.asyncio import Redis
from app.core.logger import loggers
from app.core.config import settings


class RedisClient:
    def __init__(self):
        self.client: Redis = Redis.from_url(settings.REDIS_URL, decode_responses=True)

    async def check_redis_connection(self) -> Optional[str]:
        try:
            await self.client.ping()
            return "Ok"
        except Exception as e:
            loggers.db.error(f"Error connecting to Redis: {e}")
            return None

    async def set_json(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        ttl = ttl or settings.SESSION_TTL
        try:
            # Use pipeline for atomicity
            async with self.client.pipeline() as pipe:
                await pipe.set(key, json.dumps(value))
                await pipe.expire(key, ttl, nx=True)
                await pipe.execute()
            return True
        except Exception as e:
            loggers.db.error(f"Redis set_json error for key '{key}': {e}")
            return False

    async def get_json(self, key: str) -> Optional[Any]:
        try:
            data = await self.client.get(key)
            return json.loads(data) if data else None
        except Exception as e:
            loggers.db.error(f"Redis get_json error for key '{key}': {e}")
            return None

    async def delete(self, key: str) -> bool:
        try:
            result = await self.client.delete(key)
            return result > 0
        except Exception as e:
            loggers.db.error(f"Redis delete error for key '{key}': {e}")
            return False

    async def exists(self, key: str) -> bool:
        try:
            result = await self.client.exists(key)
            return result > 0
        except Exception as e:
            loggers.db.error(f"Redis exists check failed for key '{key}': {e}")
            return False


# Instantiate global client
redis_client = RedisClient()
