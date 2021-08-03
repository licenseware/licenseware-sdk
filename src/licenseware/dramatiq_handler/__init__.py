"""
Initialize dramatiq redis broker with Flask app instance
Add to builtins functions DramatiqEvent function so it can be used in all application without any imports

Ex:

# main.py
from app.main import create_app
from workers.main.controller import process_redis_event   
from dramatiq_handler import initialize_context

app = create_app()
initialize_context(app, process_redis_event)


app.register_blueprint(blueprint)


# any_other_file.py
        
DramatiqEvent.send(event)

Where `process_redis_event` is the event handler which will be decorated with `dramatiq.actor` decorator

"""

from .dramatiq_handler import initialize_context
