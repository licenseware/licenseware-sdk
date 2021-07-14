"""

Notification service utilities

from licenseware.notifications import notify_status

or 

from licenseware import notify_status

"""
import os, time
import requests
from licenseware.utils.log_config import log
from licenseware.decorators.auth_decorators import authenticated_machine
from licenseware.utils.urls import NOTIFICATION_SERVICE_URL, APP_ID
from licenseware.app_creator.tenant_utils import TenantUtils


@authenticated_machine
async def notify_status(event, status):
    """
        Sends a post request to registry service with the status of the data processing
    """
    
    if status == 'idle':
        # Check if there are any Running processsors before sending Idle to registry-service
        wait = 5 #sec
        for _ in range(int(3600/wait)): # 1 hour
            res, _ = TenantUtils().get_processing_status(event["tenant_id"])
            if res['status'] == 'Running':
                time.sleep(wait)
            elif res['status'] == 'Idle':
                break
            

    url = NOTIFICATION_SERVICE_URL + "/processing-status"
    
    payload = {
        'tenant_id': event["tenant_id"],
        'upload_id': event["event_type"],
        'status': status,
        'app_id': APP_ID
    }

    res = requests.post(
        url, json=payload, headers={"Authorization": os.getenv('AUTH_TOKEN')}
    )
    
    if res.status_code != 200:
        log.error("Failed to send processing status to notification-service")
