import os
from dramatiq.brokers.redis import RedisBroker


broker = RedisBroker(
    host=os.getenv('REDIS_HOST'),
    port=os.getenv('REDIS_PORT'),
    db=os.getenv('REDIS_DB_ID', 0),
    password=os.getenv('REDIS_PASSWORD', None)
)
