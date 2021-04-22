import os, logging, traceback
import requests
from loguru import logger

logger.add("file_validators.log", format="{time:YYYY-MM-DD at HH:mm:ss} [{level}] - {message}", backtrace=False, diagnose=False)


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
        logger.warning("Notification sent")
    except:
        logger.exception("\n\n\n\n-------------Failsafe traceback:\n\n")
