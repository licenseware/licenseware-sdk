import logging, traceback
from pymongo.errors import ConnectionFailure
from marshmallow import ValidationError


def failsafe(func):
    def func_wrapper(*args, **kwargs):
        try:
        
           return func(*args, **kwargs)
           
        except ConnectionFailure as err:
            logging.error(traceback.format_exc())
            return "errors with mongo connection"

        except ValidationError as err:
            logging.error(traceback.format_exc())
            return "errors on validation"

        except Exception as err:
            logging.error(traceback.format_exc())
            return str(err)

    return func_wrapper

