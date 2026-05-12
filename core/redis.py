import redis.asyncio as redis

from core.config import settings


# =========================================================
# Redis Connection Pool (ASYNC)
# =========================================================
# WHY?
# - Keeps connection reusable
# - Avoids reconnecting every request
# - Improves performance (important for auth system)
# =========================================================

# redis_client = redis.Redis(
#     host=settings.REDIS_URL.split("://")[1].split(":")[0],  
#     port=int(settings.REDIS_URL.split(":")[-1].split("/")[0]),
#     db=0,
#     decode_responses=True  # returns strings instead of bytes
# )

redis_client = redis.Redis.from_url(
    settings.REDIS_URL,
    decode_responses=True
)

# =========================================================
# Redis Dependency
# =========================================================
def get_redis():
    return redis_client

async def close_redis():
   await redis_client.close()
   print("Redis Connection Closed Successfully.")

# =========================================================
# CONNECTION TEST FUNCTION (OPTIONAL BUT USEFUL)
# =========================================================
async def check_redis_connection():
    """
    Simple health check for Redis connection
    Used during startup debugging
    """
    redis_res =  await redis_client.ping()
    if redis_res:
        print("✅✅✅ Redis Connected Successfully")
    else:
        print("❌❌❌ Redis Connection Failed:", redis_res)
    return redis_res