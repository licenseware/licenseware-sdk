import os, logging, traceback
import requests


async def notify_status(tenant_id, upload_id, status, app_id):
    """
        Sends a post request to registry service with the status of the data processing
    """
    
    url = os.getenv("NOTIFICATION_SERVICE_URL") + "/processing-status"
    
    headers = {"Authorization": os.getenv('AUTH_TOKEN')}

    payload = {
        'tenant_id': tenant_id,
        'upload_id': upload_id,
        'status': status,
        'app_id': app_id
    }

    try:
        requests.post(url, json=payload, headers=headers)
        logging.warning("Notification sent")
        logging.warning(payload)
    except:
        logging.warning(traceback.format_exc())
    