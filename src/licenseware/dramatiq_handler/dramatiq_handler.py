import dramatiq
from flask import Flask
from typing import Callable
from .redis_broker import broker
from .app_middleware import AppContextMiddleware
import builtins

#TODO if event_handlers is a list we could add them all to builtins


def initialize_context(app: Flask, event_handler: Callable):

    dramatiq.set_broker(broker)
    broker.add_middleware(AppContextMiddleware(app))
    
    dramatiq_actor = dramatiq.actor(fn=lambda *args, **kwargs: event_handler, broker=broker, max_retries=3)
    
    builtins.DramatiqEvent = dramatiq_actor
    
    return dramatiq_actor
    
