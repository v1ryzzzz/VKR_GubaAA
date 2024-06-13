from redis.asyncio import Redis

from core.config import REDIS_URL_EMAIL_CONFIRMATIONS, REDIS_URL_PASSWORD_RECOVERY


async def get_redis_email_confirmations():
    redis = await Redis.from_url(REDIS_URL_EMAIL_CONFIRMATIONS)
    yield redis
    await redis.aclose()


async def get_redis_password_recovery():
    redis = await Redis.from_url(REDIS_URL_PASSWORD_RECOVERY)
    yield redis
    await redis.aclose()
