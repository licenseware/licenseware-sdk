import dramatiq
from functools import wraps
from .redis_broker import broker
from .app_middleware import AppContextMiddleware


#Function which will handle events
dramatiq_sender = None



def dramatiq_initiator(app):
    """
        Initialize dramatiq redis broker with Flask app instance
    """
    
    dramatiq.set_broker(broker)
    broker.add_middleware(AppContextMiddleware(app))
    
    return app
    

def dramatiq_listener(func):
    """
        Default dramatiq decorator which triggers worker function
    """

    @wraps(func)
    def decorated(*args, **kwargs):   
        global dramatiq_sender 
        dramatiq_actor  = dramatiq.actor(fn=lambda *args, **kwargs: func, broker=broker, max_retries=3)
        dramatiq_sender = dramatiq_actor #populating global scope
        return dramatiq_sender
        
    return decorated

