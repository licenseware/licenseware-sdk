import logging
import os
import time
import redis

redis_connection = redis.Redis(host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"),
                               decode_responses=True)

redis_stream = os.getenv("REDIS_PROCESSING_STREAM")
last_id_key = f'{redis_stream}_last_id'

class RedisService:

    def __init__(self):
        self.event_list = []
        self.last_id = self.get_last_id()
        self.new_events = False

    @staticmethod
    def send_stream_event(event_data):
        with redis_connection as r:
            try:
                return r.xadd(redis_stream, event_data)
            except (ConnectionError, TimeoutError) as e:
                return e

    def read_stream_events(self, count=3):
        self.event_list = []
        last_event_id = None
        # logging.info(f"Reading last id from Redis - {last_event_id}")
        last_event_id = self.get_last_id()
        # #logging.warning(last_event_id)
        last_read = redis_connection.xread({redis_stream: last_event_id}, count=count)
        # #logging.warning(last_read)

        for stream_name, events in last_read:
            if events:
                self.new_events = True
                self.event_list.extend([e for e_id, e in events])
                last_id = events[-1][0]
                self.set_last_id(last_id)
            else:
                self.new_events = False

    def get_last_id(self):
        last_processed_id = last_id_in_queue = None
        try:
            last_processed_id = redis_connection.get(last_id_key)
        except (TypeError, redis.exceptions.DataError):
            last_id_in_queue = redis_connection.xrevrange(redis_stream, '+', '-', 1)[0][0]
        last_id = last_processed_id or last_id_in_queue
        #logging.warning(last_id)
        return last_id or '0-0'

    def set_last_id(self, last_id):
        #logging.warning(f'Saving last id {last_id}')
        return redis_connection.set(last_id_key, last_id)
