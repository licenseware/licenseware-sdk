"""

Register a processing file/uploader attributes.

from licenseware import Uploader, reason_response
or 
from licenseware.registry.uploader import Uploader, reason_response

"""


import os
import logging
import requests
from licenseware.utils import RedisService, save_file
from licenseware.quota import Quota


def reason_response(reason, valid_fname, valid_contents, filename_nok_msg='Filename is not valid.'):
    """
        :reason         - bool affects response if True will be in dict format else bool
        :valid_fname    - the response from validate_filename function from file_validators
        :valid_contents - the response from GeneralValidator.validate()
    """

    if reason:
        if not valid_fname: 
            return {
                'status': 'fail',
                'message': filename_nok_msg
            }
        else:
            return valid_contents
    else:
        return all([valid_fname, valid_contents])




class Uploader:

    """
        This library is used to register/store information about files 
        that will be uploaded and processed.

        Use case:
        ```py

        UniqueName = Uploader(
            app_id="name-service",
            upload_name="Short description",
            uploader_id="UniqueName",
            description="Long description",
            upload_url="/UniqueName/files",
            upload_validation_url='/UniqueName/validation',
            validate_upload_function=receive_files_UniqueName, #function that validates file contents and file name
            validate_filename_function=validate_UniqueName, #function that validates file contents and file name
            quota_collection_name=None, # if not specified will be computed from app_id (check code)
            unit_type=None, # if not specified uploader_id will be taken
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
        - APP_BASE_PATH
        - APP_URL_PREFIX      
        - REGISTRY_SERVICE_URL
        - AUTH_TOKEN
                
    """

    def __init__(
        self,
        app_id,
        upload_name,
        uploader_id,
        description,
        upload_url,
        upload_validation_url,
        status_check_url,
        quota_validation_url,
        history_url,
        validate_upload_function,
        validate_filename_function,
        quota_collection_name=None,
        unit_type=None,
        status="idle",
        icon="default.png",
    ):

        self.app_id = app_id
        self.upload_name = upload_name
        self.uploader_id = uploader_id
        self.description = description
        self.upload_url = upload_url
        self.upload_validation_url = upload_validation_url
        self.quota_validation_url = quota_validation_url
        self.status_check_url = status_check_url
        self.history_url = history_url
        self.status = status
        self.icon = icon
        self.validate_upload = validate_upload_function
        self.validate_filename = validate_filename_function
        
        self.quota_collection_name = quota_collection_name or str(app_id).split("-")[0].upper() + "Utilization"
        self.quota = Quota(self.quota_collection_name)        
        self.unit_type = unit_type or self.uploader_id
        
        self.base_url = os.getenv("APP_BASE_PATH") + os.getenv("APP_URL_PREFIX") + '/uploads'
        self.registration_url = f'{os.getenv("REGISTRY_SERVICE_URL")}/uploaders'
        self.auth_token = os.getenv('AUTH_TOKEN')


        

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
                "uploader_id": self.uploader_id,
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


    def upload_files(self, request_obj, event_type=None):
        """ 
            Upload files from request.

            :event_type if None uploader_id will be taken as an event_type
        """
        self.quota
        return self._upload_response(
            request_obj,  
            event_type=event_type or self.uploader_id
        )


    def validate_filenames(self, request_obj):
        """
            Validate filenames from flask request.
        """
        
        msg, status = self._filenames_response(request_obj)

        response = self.quota.check_quota(
            request_obj.headers.get("TenantId"), 
            unit_type='fmw_archive', 
            number_of_units=msg['units']
        )

           

    def _filenames_response(self, request_obj, filename_ok_msg='Filename is valid.', filename_nok_msg='Filename is not valid.'):

        filenames = request_obj.json

        if not isinstance(filenames, list) and filenames:
            return {'status': 'fail', 'message': 'Must be a list of filenames.'}, 400

        validation, accepted_files = [], []
        for filename in filenames:
            status, message = 'fail', filename_nok_msg
            if self.validate_filename(filename):
                accepted_files.append(filename)
                status, message = 'success', filename_ok_msg
                
            validation.append({
                "filename": filename, "status": status, "message": message
            })
        
        if not accepted_files:
            return {
                'status': 'fail', 
                'message': filename_nok_msg,
                'validation': validation,
                'units': 0
            }, 400

        return {
            'status': 'success', 
            'message': 'Filenames are valid.',
            'validation': validation,
            'units': len(accepted_files)
        }, 200


    def _upload_response(self, request_obj, event_type):

        file_objects = request_obj.files.getlist("files[]")
        if not isinstance(file_objects, list) and file_objects:
            return {"status": "fail", "message": "key needs to be files[]"}, 400
            
        saved_files, validation = [], []
        for file in file_objects:
            res = self.validate_upload(file, reason=True)
            if res['status'] == "success":
                filename = save_file(file, request_obj.headers.get("TenantId"))
                saved_files.append(filename)
            else:
                filename = file.filename
            
            validation.append({
                "filename": filename, "status": res['status'], "message": res['message']
            })


        if not saved_files:
            return {
                "status": "fail", "message": "no valid files provided", "validation": validation
            }, 400


        RedisService.send_stream_event({
            "tenant_id": request_obj.headers.get("TenantId"),
            "files": ",".join(saved_files),
            "event_type": event_type
        })

        return {"status": "success", "message": "files uploaded successfuly", 
            "units": len(saved_files), 
            "validation": validation
        }, 200



