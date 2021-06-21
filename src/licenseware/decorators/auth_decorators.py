import os
import requests
from functools import wraps
from datetime import datetime

try:
    from flask import request
except:
    pass  # we are on the worker side

from licenseware.utils.log_config import log
from licenseware.auth import Authenticator

# Auth decorators

url_auth_check = os.getenv('AUTH_SERVICE_URL', '') + "/verify"
url_machine_check = os.getenv('AUTH_SERVICE_URL', '') + "/machine_authorization"

env = os.getenv("ENVIRONMENT")


def authorization_check(f):
    """
        Checks if a user is authorized
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            headers = {"TenantId": request.headers.get("TenantId"),
                       "Authorization": request.headers.get("Authorization")}
            response = requests.get(url=url_auth_check, headers=headers)
            if response.status_code != 200:
                log.warning("Unauthorized user")
                return {"status": "unauthorized"}, 401
            return f(*args, **kwargs)
        except KeyError:
            return {"Missing Tenant or Authorization information"}, 403

    return decorated


def machine_check(f):
    """
        Checks if a machine is authorized
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            headers = {"Authorization": request.headers.get("Authorization")}
            response = requests.get(url=url_machine_check, headers=headers)
            if response.status_code != 200:
                return {"status": "unauthorized"}, 401
            return f(*args, **kwargs)
        except KeyError:
            log.warning("Unauthorized machine")
            return {"Missing Authorization information"}, 403

    return decorated


def authenticated_machine(f):
    """
        Refreshes the authentication token before making a request
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            Authenticator().connect()
            return f(*args, **kwargs)
        except KeyError:
            log.warning("Could not refresh token")
            return {"Could not refresh token"}, 403

    return decorated
