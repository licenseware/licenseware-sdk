import asyncio
import logging
import multiprocessing
import time
from .redis_service import RedisService



class RedisEventDispacher:
    """

    Read Redis stream events and delegate them to an event_handler.

    from licenseware import RedisEventDispacher

    def main():
        e = RedisEventDispacher(event_handler=Controller.process_redis_event)
        e.listen()

    `event_handler` function should receive only one argument

    """

    def __init__(self, event_handler):
        self.event_handler = event_handler


    def listen(self):
        while True:
            redis_service = RedisService()
            redis_service.read_stream_events()
            if redis_service.new_events:
                logging.warning(f"\n------ {len(redis_service.event_list)} NEW REDIS EVENTS")
                p = multiprocessing.Process(target=self._process_event, args=(redis_service,), daemon=True)
                p.start()          
            time.sleep(1) #Go easy on CPU


    def _process_event(self, redis_service):
        events = redis_service.event_list
        loop = asyncio.get_event_loop()
        logging.warning("Processing...")
        logging.warning(events)
        loops = [loop.create_task(self.event_handler(event)) for event in events]
        loop.run_until_complete(asyncio.wait(loops))
        return True

