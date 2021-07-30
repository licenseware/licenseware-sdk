"""

Notify registry about the status of a uploader status
with either 'running' or 'idle' statuses.
If status is 'running' all related reports to this upload 
in the frontend will have a running icon.

new_event = {
    'tenant_id': '1f4ff303-xxxx-xxxx-xxxx-a8ba27c511ff', 
    'upload_id': 'cpuq', 
    'status': 'idle', 
    'app_id': 'ifmp-service'
}
        
"""

import os
import requests
from .log_config import log
from .urls import REGISTRY_SERVICE_URL
# from licenseware.decorators.auth_decorators import authenticated_machine
from licenseware.auth import Authenticator



# @authenticated_machine #causes circular import
def update_registry(new_event):
    
    Authenticator.connect()    

    log.info(f"Sending update to registry, data: {new_event}")
    payload = {'data': [new_event]}

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

