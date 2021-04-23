import os
import redis



redis_connection = redis.Redis(
    host=os.getenv("REDIS_HOST", "http://localhost"),
    port=os.getenv("REDIS_PORT", '6379')
)

redis_stream = os.getenv("REDIS_PROCESSING_STREAM", "default_redis_stream")


class RedisService:

    @staticmethod
    def send_stream_event(event_data):
        with redis_connection as r:
            try:
                return r.xadd(redis_stream, event_data)
            except (ConnectionError, TimeoutError) as e:
                print(e)
                return e
