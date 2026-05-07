import json
from datetime import datetime
from uuid import UUID
from core.redis import redis_client
from infrastructure.redis.generate_key import generate_cache_key


class RedisCacheService:

    def _json_default(self, obj):
        # Make cached payloads JSON-safe (UUID, datetime, etc.)
        if isinstance(obj, UUID):
            return str(obj)
        if isinstance(obj, (datetime,)):
            return obj.isoformat()
        return str(obj)

    # =====================================================
    # SET VALUE
    # =====================================================
    async def set(self, key: str, value: any, ttl: int = None):
        """
        Store value in Redis with optional TTL
        """

        payload = {
            "data": value,
            "__cachedAt": datetime.utcnow().isoformat()
        }

        if ttl:
            await redis_client.setex(key, ttl, json.dumps(payload, default=self._json_default))
        else:
            await redis_client.set(key, json.dumps(payload, default=self._json_default))

    # =====================================================
    # GET VALUE
    # =====================================================
    async def get(self, key: str):
        """
        Retrieve value with metadata
        """

        result = await redis_client.get(key)

        if not result:
            return None

        data = json.loads(result)

        return {
            "data": data.get("data"),
            "cachedAt": data.get("__cachedAt")
        }

    # =====================================================
    # DELETE KEY
    # =====================================================
    async def del_key(self, key: str):
        await redis_client.delete(key)

    # =====================================================
    # EXISTS
    # =====================================================
    async def exists(self, key: str):
        return await redis_client.exists(key) == 1

    # =====================================================
    # PREFIX DELETE (SCAN STREAM - SAFE)
    # =====================================================
    async def del_by_prefix(self, prefix: str):
        async for key in redis_client.scan_iter(match=f"{prefix}*"):
            await redis_client.delete(key)

    # =====================================================
    # GET OR SET (VERY IMPORTANT)
    # =====================================================
    async def get_or_set(self, key, fetch_fn, ttl=300):
        """
        If cache exists → return it
        else → fetch, store, return
        """

        cached = await self.get(key)

        if cached:
            return {"data": cached["data"], "cached": True}

        fresh = await fetch_fn()

        await self.set(key, fresh, ttl)

        return {"data": fresh, "cached": False}


# Singleton instance 
redis_service = RedisCacheService()