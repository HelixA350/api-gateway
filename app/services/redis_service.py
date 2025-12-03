from arq.connections import RedisSettings
import os

redis_settings = RedisSettings(
    host=os.getenv("REDIS_HOST"),
    port = os.getenv("REDIS_PORT"),
)
