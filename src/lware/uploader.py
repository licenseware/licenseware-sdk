import os
import logging
import requests


class Uploader:

    """
        This library is used to register/store information about files 
        that will be uploaded and processed.

        Use case:
        ```py

        from uploader import Uploader

        UniqueName = Uploader(
            app_id="name-service",
            upload_name="Short description",
            upload_id="UniqueName",
            description="Long description",
            upload_url="/UniqueName/files",
            upload_validation_url='/UniqueName/validation',
            quota_validation_url='/quota/UniqueName',
            status_check_url='/UniqueName/status',
            history_url='/UniqueName/history'
        )

        response, status_code = UniqueName.register_uploader()

        if status_code == 200:
            # uploader registration succeeded


        ```

        Before calling `register_uploader` app must be logged in.
            
        The following environment variables are expected:
        - APP_BASE_PATH, APP_URL_PREFIX  or `uploads_base_url` parameter filled;     
        - REGISTRY_SERVICE_URL or `registration_url` parameter filled.
        - `AUTH_TOKEN` or `auth_token` parameter filled.
                

    """

    def __init__(
        self,
        app_id,
        upload_name,
        upload_id,
        description,
        upload_url,
        upload_validation_url,
        status_check_url,
        quota_validation_url,
        history_url,
        status="Idle",
        icon="default.png",
        uploads_base_url=None,
        registration_url=None,
        auth_token=None,
    ):

        self.app_id = app_id
        self.upload_name = upload_name
        self.upload_id = upload_id
        self.description = description
        self.upload_url = upload_url
        self.upload_validation_url = upload_validation_url
        self.quota_validation_url = quota_validation_url
        self.status_check_url = status_check_url
        self.history_url = history_url
        self.status = status
        self.icon = icon
    
        self.base_url = uploads_base_url or os.getenv("APP_BASE_PATH") + os.getenv("APP_URL_PREFIX") + '/uploads'
        self.registration_url = registration_url or f'{os.getenv("REGISTRY_SERVICE_URL")}/uploaders'
        self.auth_token = auth_token or os.getenv('AUTH_TOKEN')
        

    def register_uploader(self):

        if not self.auth_token:
            logging.warning('Uploader not registered, no AUTH_TOKEN available')
            return {
                "status": "fail", 
                "message": "Uploader not registered, no AUTH_TOKEN available" 
            }, 403


        payload = {
            'data': [{
                "app_id": self.app_id,
                "upload_name": self.upload_name,
                "upload_id": self.upload_id,
                "description": self.description,
                "upload_url": self.base_url + self.upload_url,
                "upload_validation_url": self.base_url + self.upload_validation_url,
                "quota_validation_url": self.base_url + self.quota_validation_url,
                "status_check_url": self.base_url + self.status_check_url,
                "history_url": self.base_url + self.history_url,
                "status": self.status,
                "icon": self.icon,
            }]
        }

        logging.warning(payload)
        
        headers = {"Authorization": self.auth_token}
        registration = requests.post(url=self.registration_url, json=payload, headers=headers)

        logging.warning(registration.content)

        if registration.status_code == 200:
            return {
                "status": "success",
                "message": "Uploader register successfully"
            }, 200

        else:
            logging.warning("Could not register uploader")
            return {
                "status": "fail",
                "message": "Could not register uploader"
            }, 400
    