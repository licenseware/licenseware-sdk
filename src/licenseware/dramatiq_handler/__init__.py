"""

This package makes available for use 2 main functions
- dramatiq_initiator
- dramatiq_listener

Usage:

# API init
# main/__init__py

from flask import Flask
from licenseware.dramatiq_handler import dramatiq_initiator

def create_app():

    app = Flask(__name__)
    app = dramatiq_initiator(app) 
    
    return app


# WORKER init
# main/controller.py

from licenseware.dramatiq_handler import dramatiq_listener

@dramatiq_listener
def process_redis_event(event):
    mapping = {
        "ofmw_archive": process_event_ofmw_archives
    }

    event_type = event["event_type"]
    sync_notify_status(
        tenant_id=event['tenant_id'],
        upload_id=event['event_type'],
        status='running',
        app_id='fmw-service'
    )
    processed_data = None
    try:
        processed_data = mapping[event_type](event)
    except Exception as e:
        log.error(e)
    finally:
        sync_notify_status(
            tenant_id=event['tenant_id'],
            upload_id=event['event_type'],
            status='idle',
            app_id='fmw-service'
        )
    return processed_data


# Sending events

#TODO



"""


from .dramatiq_handler import dramatiq_initiator, dramatiq_listener
