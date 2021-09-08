"""
    
Licenseware components authentification.


from licenseware import Authenticator

Authenticator.connect() #returns a tuple json, status code 


Requirements:

Set login values in environment variables:
- LWARE_IDENTITY_USER (the email)
- LWARE_IDENTITY_PASSWORD (the password)
- AUTH_SERVICE_URL (the url for authentication)
- AUTH_SERVICE_USERS_URL_PATH (route auth to users)


This is just for internal licenseware use:
- AUTH_SERVICE_MACHINES_URL_PATH (route auth to be used between services)

"""

import os
import requests
from requests.adapters import HTTPAdapter
from requests.packages import urllib3
from datetime import datetime, timedelta
from functools import wraps
from licenseware.utils.log_config import log

retry_strategy = urllib3.Retry(
    total=3
)
adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("https://", adapter)
http.mount("http://", adapter)


class Authenticator:

    def __init__(self):

        self.email = os.getenv("LWARE_IDENTITY_USER")
        self.password = os.getenv("LWARE_IDENTITY_PASSWORD")
        self.auth_url = os.getenv("AUTH_SERVICE_URL")

        if os.getenv("AUTH_SERVICE_MACHINES_URL_PATH"):
            route = os.getenv('AUTH_SERVICE_MACHINES_URL_PATH')
        else:
            route = os.getenv('AUTH_SERVICE_USERS_URL_PATH')

        self.auth_url = self.auth_url + route


    @classmethod
    def connect(cls):
        """
            Connects to licenseware and saves in environment variables auth tokens.
        """

        response, status_code = cls()._login()

        if status_code == 200:
            os.environ['AUTH_TOKEN'] = response.get("Authorization", "Authorization not found")
            os.environ['TENANT_ID'] = response.get("TenantId", "TenantId not found")
            os.environ['APP_AUTHENTICATED'] = 'true'
            os.environ['AUTH_TOKEN_DATETIME'] = datetime.utcnow().isoformat()
        else:
            os.environ['APP_AUTHENTICATED'] = 'false'
            log.error(response)
            
        return response

    def _login(self):

        identity = "machine_name" if os.getenv("AUTH_SERVICE_MACHINES_URL_PATH") else "email"
        payload = {
            identity: self.email,
            "password": self.password
        }

        response = http.post(url=f"{self.auth_url}/login", json=payload)

        if response.status_code == 200:
            return response.json(), 200
        else:
            return self._create_machine()

    def _create_machine(self):

        if not os.getenv('AUTH_SERVICE_MACHINES_URL_PATH'):
            return {
                       "status": "fail",
                       "message": "Please create an account before using this Licenseware SDK."
                   }, 403

        payload = {
            "machine_name": self.email,
            "password": self.password
        }

        response = http.post(url=f'{self.auth_url}/create', json=payload)

        if response.status_code == 201:
            return response.json(), 201

        return {
                   "status": "fail",
                   "message": "Could not create account",
               }, 500
