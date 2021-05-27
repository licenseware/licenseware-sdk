"""

Notification service utilities

from licenseware.notifications import notify_status

or 

from licenseware import notify_status

"""

import os
import requests
from licenseware.utils.log_config import log


async def notify_status(tenant_id, upload_id, status, app_id=None):
    """
        Sends a post request to registry service with the status of the data processing
    """
    
    if not app_id: app_id = os.getenv("LWARE_IDENTITY_USER")
    
    url = os.getenv("NOTIFICATION_SERVICE_URL") + "/processing-status"
    
    payload = {
        'tenant_id': tenant_id,
        'upload_id': upload_id,
        'status': status,
        'app_id': app_id
    }

    res = requests.post(
        url, json=payload, headers={"Authorization": os.getenv('AUTH_TOKEN')}
    )

    log.info("------ notify_status:" + str(res.content))
    