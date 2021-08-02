import dramatiq
from functools import wraps
from .redis_broker import broker
from .app_middleware import AppContextMiddleware



def dramatiq_initiator(app):
    """
        Initialize dramatiq redis broker with Flask app instance
    """
    
    dramatiq.set_broker(broker)
    broker.add_middleware(AppContextMiddleware(app))
    
    return app
    

def dramatiq_listener(f):
    """
        Default dramatiq decorator which triggers worker function
    """

    @wraps(f)
    def decorated(*args, **kwargs):   
        return dramatiq.actor(fn=f, broker=broker, max_retries=3)
        
    return decorated

