from licenseware.utils.log_config import log
from functools import wraps
from licenseware.utils.redis_service import redis_connection as rd
from licenseware.notifications import notify_status


def send_notification(f):
    @wraps(f)
    async def decorated(*args, **kwargs):
        event = args[0]
        number_key = f"number_of_running_events_{event['tenant_id']}_{event['event_type']}"
        status_key = f"uploader_status_{event['tenant_id']}_{event['event_type']}"
        current_status = rd.get(status_key)
        if current_status == 'idle':
            await notify_status(
                tenant_id=event['tenant_id'],
                upload_id=event['event_type'],
                status='running'
            )
            rd.set(status_key, 'running')
        rd.incrby(number_key, 1)
        result = await f(*args, **kwargs)
        rd.decrby(number_key, 1)
        currently_running = rd.get(number_key)
        if currently_running == 0:
            await notify_status(
                tenant_id=event['tenant_id'],
                upload_id=event['event_type'],
                status='idle'
            )
            rd.set(status_key, 'idle')
        return result

    return decorated
