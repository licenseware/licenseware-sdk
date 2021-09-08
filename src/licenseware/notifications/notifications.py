"""

Notification service utilities

from licenseware.notifications import notify_status

or 

from licenseware import notify_status

"""
import os
import time
import traceback
from licenseware.utils.log_config import log
from licenseware.decorators.auth_decorators import authenticated_machine
from licenseware.utils.urls import APP_ID
from licenseware.app_creator.tenant_utils import TenantUtils
from licenseware.notifications.notifications_handler import EventNotificationsHandler


def backward_compatibility(**kparams):
    # TODO notify_status needs only 2 params: event and status
    # upload_id should be the same with event_type
    # app_id should be unique Unique-service
    # previous: event["tenant_id"], "ofmw_lms_collection", 'started', app_id='fmw-service'
    # new: event, status

    if isinstance(kparams['tenant_id'], dict):
        return kparams['tenant_id'], kparams['status'] or kparams['event_type']
    else:
        return kparams, kparams['status'] or kparams['event_type']

@authenticated_machine
def sync_notify_status(tenant_id, upload_id=None, status=None, app_id=None):
    """
        Sends a post request to registry service with the status of the data processing
    """

    event, status = backward_compatibility(
        **dict(tenant_id=tenant_id, event_type=upload_id, status=status, app_id=app_id)
    )

    if status == 'idle':
        res, _ = TenantUtils().get_uploader_status(
                event["tenant_id"], event['event_type'])
        if res['status'] == 'Running':
            return None
    notif_event = {
        'tenant_id': event["tenant_id"],
        'upload_id': event["event_type"],
        'status': status,
        # added for backward compatibility
        'app_id': app_id or APP_ID.replace('worker', 'service')
    }
    
    if 'local' in os.getenv("ENVIRONMENT", ""):
            notif_event['app_id'] = f"{app_id}-{os.getenv('PERSONAL_PREFIX', 'local')}"
            notif_event['upload_id'] = f"{event['event_type']}-{os.getenv('PERSONAL_PREFIX', 'local')}"

    try:
        return EventNotificationsHandler(notif_event).status_check()
    except Exception:
        log.error(traceback.format_exc())
        return None


@authenticated_machine
async def notify_status(tenant_id, upload_id=None, status=None, app_id=None):
    """
        Sends a post request to registry service with the status of the data processing
    """

    event, status = backward_compatibility(
        **dict(tenant_id=tenant_id, event_type=upload_id, status=status, app_id=app_id)
    )

    if status == 'idle':
        # Check if there are any Running processsors before sending Idle to registry-service
        wait = 5  # sec
        for _ in range(int(3600/wait)):  # 1 hour
            res, _ = TenantUtils().get_uploader_status(
                event["tenant_id"], event['event_type'])
            if res['status'] == 'Running':
                time.sleep(wait)
            elif res['status'] == 'Idle':
                break

    notif_event = {
        'tenant_id': event["tenant_id"],
        'upload_id': event["event_type"],
        'status': status,
        # added for backward compatibility
        'app_id': app_id or APP_ID.replace('worker', 'service')
    }

    try:
        return EventNotificationsHandler(notif_event).status_check()
    except Exception:
        log.error(traceback.format_exc())
        return None
