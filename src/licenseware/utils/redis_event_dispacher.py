import asyncio
import multiprocessing
import time
from .redis_service import RedisService
from .cron_jobs import cron_jobs_list
from .log_config import log
from concurrent.futures import ProcessPoolExecutor


minutes = lambda minutes: 60 * minutes


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
        
        cron_clock = 0
        
        while True:
            redis_service = RedisService()
            redis_service.read_stream_events()
            if redis_service.new_events:
                # log.info(f"\n------ {len(redis_service.event_list)} NEW REDIS EVENTS")
                p = multiprocessing.Process(target=self._process_event, args=(redis_service,), daemon=True)
                p.start()       
                   
            time.sleep(1) #Go easy on CPU
            
            # Cron tasks 
            cron_clock += 1
            if cron_clock == minutes(120): #each 2 hours
                with ProcessPoolExecutor() as executor:
                    for cron_job in cron_jobs_list:
                        executor.submit(cron_job)  #execute cron jobs    
                         
                cron_clock = 0 #reset clock
            
            
    def _process_event(self, redis_service):
        events = redis_service.event_list
        loop = asyncio.get_event_loop()
        log.info("Processing...")
        log.info(events)
        loops = [loop.create_task(self.event_handler(event)) for event in events]
        loop.run_until_complete(asyncio.wait(loops))
        return True

