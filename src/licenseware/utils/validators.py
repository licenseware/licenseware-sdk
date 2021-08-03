from licenseware.serializer import EventSchema


def validate_event(event):
    EventSchema().load(event)
        
    