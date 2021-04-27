"""

Useful decoratators.

from licenseware.decorators import (
    failsafe,
    authorization_check,
    machine_check,
    header_doc_decorator
)

or 

from licenseware import decorators


"""


import os
import logging
import requests
from functools import wraps
from flask import request
from loguru import logger

logger.add("failsafe.log", format="{time:YYYY-MM-DD at HH:mm:ss} [{level}] - {message}", backtrace=False, diagnose=False)


def failsafe(*dargs, fail_code=0, success_code=0):
    """
        Prevents a function to raise an exception and break the app.
        Returns a string with the exception and saves the traceback in failsafe.log
        If fail_code or success_code is specified then a json response will be returned.
        
        @failsafe
        def fun1(): raise Exception("test")
        print(fun1())
        # >>test

        @failsafe(fail_code=500)
        def fun2(): raise Exception("test")
        print(fun2())
        # >> ({'status': 'Fail', 'message': 'test'}, 500)

        @failsafe(fail_code=500, success_code=200)
        def fun3(): return "test"
        print(fun3())
        # >> ({'status': 'Success', 'message': 'test'}, 200)
        
    """
    
    def _decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                response = f(*args, **kwargs)
                if success_code:
                    return {"status": "Success", "message": response}, success_code
                return response
            except Exception as err:
                logger.exception("\n\n\n\n-------------Failsafe traceback:\n\n")
                if fail_code:
                    return {"status": "Fail", "message": str(err)}, fail_code
                return str(err)
        return wrapper

    return _decorator(dargs[0]) if dargs and callable(dargs[0]) else _decorator




# Auth decorators

url_auth_check = os.getenv('AUTH_SERVICE_URL', '') + "/verify"
url_machine_check =  os.getenv('AUTH_SERVICE_URL', '') + "/machine_authorization"  

env = os.getenv("ENVIRONMENT")

def authorization_check(f):
    """
        Checks if a user is authorized
    """
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
    """
        Checks if a machine is authorized
    """
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
    """
        Adds auth parameters to header 
    """
    parser = _api.parser()
    parser.add_argument('Authorization', location='headers')
    parser.add_argument('TenantId', location='headers')
    return parser
