import requests
import logging
import os


class Authenticator:

    """
    
    This class can be used for Licenseware authentification.

    Set login values in environment variables:
    - LWARE_IDENTITY_USER (the email)
    - LWARE_IDENTITY_PASSWORD (the password)
    - AUTH_SERVICE_URL (the url for login)

    Otherwise you can pass them directly into Authenticator (not recommended).
    - email
    - password
    - auth_url

    If you are using environment variables you can login like this:
    ```py
    
    from lware.auth import Authenticator

    response = Authenticator.connect()
    # check response

    ``` 

    Or like this if you are not using environment variables:
    
    ```py
    
    from lware.auth import Authenticator

    response = Authenticator(
        email="email@company.com", 
        password="not recommended", 
        auth_url="https://licenseware.io/auth"
    ).connect()

    # check response
    

    ```

    """

    def __init__(
        self, 
        email=None, 
        password=None, 
        auth_url=None,
        debug=False
    ):
        
        self.email    = email    or os.getenv("LWARE_IDENTITY_USER")
        self.password = password or os.getenv("LWARE_IDENTITY_PASSWORD")
        self.auth_url = auth_url or os.getenv("AUTH_SERVICE_URL")

        if os.getenv('AUTH_SERVICE_MACHINES_URL_PATH'):
            self.auth_url = self.auth_url + os.getenv('AUTH_SERVICE_MACHINES_URL_PATH') 
        else:
            route = os.getenv('AUTH_SERVICE_USERS_URL_PATH') or '/users'
            self.auth_url = self.auth_url + route

        self.debug = debug

        
    @classmethod
    def connect(cls):
        response, status_code = cls().login()
        cls().show_logs(response, status_code)
        
        if status_code == 200:
            cls().show_logs('Logged in')
            os.environ['AUTH_TOKEN'] = response.get("Authorization", "Authorization not found")
            os.environ['TENANT_ID'] = response.get("TenantId", "TenantId not found")
            os.environ['APP_AUTHENTICATED'] = 'true'
        else:
            os.environ['APP_AUTHENTICATED'] = 'false'
            cls().show_logs('Could not login')
        
        return response


    def login(self):

        identity = "email" if "/auth/users" in self.auth_url else "machine_name"
        payload = {
            identity: self.email,
            "password": self.password
        }
        
        self.show_logs(payload)
        response = requests.post(url=f"{self.auth_url}/login", json=payload)
        self.show_logs(response.content)

        if response.status_code == 200:
            return response.json(), 200
        else:
            return self.create_machine()


    def create_machine(self):

        if not os.getenv('AUTH_SERVICE_MACHINES_URL_PATH'):
            return {
                "status": "fail", 
                "message": "Please create an account before using this sdk."
            }, 403

        payload = {
            "machine_name": self.email,
            "password": self.password
        }
        
        self.show_logs(payload)
        response = requests.post(url=f'{self.auth_url}/create', json=payload)
        
        if response.status_code == 201:
            return response.json()
    
        self.show_logs(response.content)
        return {
            "status": "fail",
            "message": "Could not create user",
        }, 500
            
        
    def show_logs(self, *debug_info):
        if self.debug: 
            debug_info = " ; ".join([str(info) for info in debug_info])
            logging.warning(debug_info)

