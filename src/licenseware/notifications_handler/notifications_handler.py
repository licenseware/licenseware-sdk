"""

1. Create Redis Key from event data:

event = {
    'tenant_id': 'the_tenant_id',
    'upload_id': 'the_event_type',
    'status': status,
    'app_id': "the_app_id"
}

self._key = f"{event['app_id']}_{event['upload_id']}_{event['tenant_id']}"


2. Get old data from Redis based on _key:
    2.1. If old data not found for _key set 'first_time' to True
    2.2. If old data has status "running" and new data has status "idle": set new data on _key - SEND notification to registry 
    2.3. If old data has status "idle" and new data has status "running": set new data on _key - SEND notification to registry 
    2.4. If old data has status "running" and new data has status "running"  and 'first_time' is True: set new data on _key - SEND notification to registry 
    2.5. Else Ignore the rest of the cases 
    
    Works like a light swich once ON you can set it only to OFF and vice-versa
    
    
Should work for most cases, but running/idle statuses may not be corespondent to each other.

Ex:
Let's say we have for a key the following list of statuses we get from worker:

stats = ['running', 'running', 'idle', 'running', 'idle', 'idle', 'running', 'idle']  
  
'running' at index 0 may corespond to any other 'idle' following status 
'running' at index 0 may corespont to 'idle' at index 2 or 'idle' at index 4 or 5


But since each 'running' status will have at some point an 'idle' status I think it's fine.


"""

import datetime
from licenseware import log
from licenseware.utils.redis_service import redis_connection as rd
import os, json, requests
from licenseware.decorators.auth_decorators import authenticated_machine
from licenseware.utils.urls import REGISTRY_SERVICE_URL




class EventNotificationsHandler:
    
    def __init__(self, event):
        self.new_event = event
        self.old_event = None
        self._key = f"{event['app_id']}_{event['upload_id']}_{event['tenant_id']}".replace('-', '_')
        log.debug(event)
        
        self.set_old_event()
        
        
    def status_check(self):
        
        old_new_status = [self.old_event['status'], self.new_event['status']]
        
        if old_new_status == ['running', 'idle']:
            self.save()
            return self.update_registry()
        
        if old_new_status == ['idle', 'running']:
            self.save()
            return self.update_registry()
        
        if set(old_new_status) == {'running'} and self.old_event['first_time']:
            self.save()
            return self.update_registry()
    
        return {'message': 'no need to update registry'}, 200
          
        
    def set_old_event(self):
        
        if rd.exists(self._key) == 1:
            self.old_event = json.loads(rd.get(self._key))
        else:
            self.old_event = {
                'status': self.new_event['status'],
                # 'last_update': '2020-07-09T14:52:25.261393', #An old FIXED iso date
                'first_time': True
            }
        
        
    def save(self):
        log.debug(self.serialize())
        rd.set(self._key, self.serialize())

    def serialize(self):
        return json.dumps({
            '_key': self._key,
            'status': self.new_event['status'],
            # 'last_update': datetime.datetime.now().isoformat(), #maybe later for a timeout?
            'first_time': False
        }, default=str)


    @authenticated_machine
    def update_registry(self):
        log.info(f"Sending update to registry, data: {self.new_event}")
        payload = {'data': [self.new_event]}

        response = requests.post(
            url= REGISTRY_SERVICE_URL + '/uploaders/status', 
            json=payload, 
            headers={"Authorization": os.getenv('AUTH_TOKEN')}
        )

        if response.status_code == 200:
            log.info("Notification registry service success!")
            return {"status": "success", "message": payload}, 200
        else:
            log.warning("Notification registry service failed!")
            return {"status": "fail", "message": payload}, 500


