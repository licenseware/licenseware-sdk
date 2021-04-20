import os
import logging
import requests
import logging, traceback
from pymongo.errors import ConnectionFailure
from marshmallow import ValidationError
from functools import wraps
from flask import request



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



# Auth decorators

url_auth_check = f"{os.getenv('AUTH_SERVICE_URL')}/verify"
url_machine_check =  f"{os.getenv('AUTH_SERVICE_URL')}/machine_authorization"  

env = os.getenv("ENVIRONMENT")

def authorization_check(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if env is not None and env != "local":
            try:
                headers = {"TenantId": request.headers.get("TenantId"), "Authorization": request.headers.get("Authorization")}
                response = requests.get(url=url_auth_check, headers=headers)
                if response.status_code != 200:
                    logging.warning("Unauthorized")
                    return {"status": "unauthorized"}, 401
                return f(*args, **kwargs)
            except KeyError:
                return {"Missing Tenant or Authorization information"}, 403
        else:
            return f(*args, **kwargs)
    return decorated


def machine_check(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if env is not None and env != "local":
            try:
                headers = {"Authorization": request.headers.get("Authorization")}
                response = requests.get(url=url_machine_check, headers=headers)
                if response.status_code != 200:
                    return {"status": "unauthorized"}, 401
                return f(*args, **kwargs)
            except KeyError:
                return {"Missing Authorization information"}, 403
        else:
            return f(*args, **kwargs)
    return decorated



def header_doc_decorator(_api):
    parser = _api.parser()
    parser.add_argument('Authorization', location='headers')
    parser.add_argument('TenantId', location='headers')
    return parser
