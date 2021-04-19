import logging
import os
import traceback

import requests

from ..util.data_utils import (
    get_activated_tenants,
    get_tenants_with_data
)


class AppDefinition:

    def __init__(self, id, name, description, icon, app_activation_url):
        self.id = id
        self.name = name
        self.description = description
        self.icon = icon
        self.app_activation_url = app_activation_url
        self.refresh_registration_url = os.getenv("APP_BASE_PATH") + os.getenv("APP_URL_PREFIX") + '/register_all'


    def register_app(self):
        
        if os.getenv('APP_AUTHENTICATED') != 'true':
            logging.warning('App not registered, no auth token available')
            return {
                "status": "fail",
                "message": "App not registered, no auth token available"
            }, 401


        payload = {
            'data': [{
                "app_id": self.id,
                "name": self.name,
                "tenants_with_app_activated": get_activated_tenants(),
                "tenants_with_data_available": get_tenants_with_data(),
                "description": self.description,
                "icon": self.icon,
                "refresh_registration_url": self.refresh_registration_url,
                "app_activation_url": f'{os.getenv("APP_BASE_PATH")}{os.getenv("APP_URL_PREFIX")}{self.app_activation_url}'
            }]
        }

        logging.warning(payload)
        
        url = f'{os.getenv("REGISTRY_SERVICE_URL")}/apps'
        headers = {"Authorization": os.getenv('AUTH_TOKEN')}
        registration = requests.post(url, json=payload, headers=headers)
        
        if registration.status_code != 200:
            logging.warning(f"Could not register app {self.name}")
            return { "status": "fail", "message": "Could not register app" }, 500
        
        return {"status": "success","message": "App registered successfully"}, 200
   

    def register_all(self, reports=[], uploaders=[]):
        try:
            self.register_app()
            [r.register_report() for r in reports]
            [u.register_uploader() for u in uploaders]
            return True
        except:
            logging.warning(traceback.format_exc())
            return False
