"""

Register a processing file/uploader attributes.

from licenseware import Uploader, reason_response
or 
from licenseware.registry.uploader import Uploader, reason_response


#Example on how to use reason_response function

from licenseware import GeneralValidator, validate_filename

def valid_ofmw_archive_name(archive_name):
    return validate_filename(
        fname=archive_name, 
        fname_contains=["Collection"],
        fname_endswith=[".zip", ".tar.bz2"]
    )

def valid_xxx_files(file, reason=False):
    
    valid_fname, valid_contents = None, None
    
    if isinstance(file, str):
        valid_fname = valid_ofmw_archive_name(file)
        valid_contents = True

    if "stream" in str(dir(file)):
        valid_fname = valid_ofmw_archive_name(file.filename)
        
        # Cant't check contents of archive until is opened
        valid_contents = {"status": "success", "message": "File validation succeded"} 
        
        # But if you could check contents would be something like bellow:
        # if valid_fname:
        #     valid_contents = GeneralValidator(
        #         input_object=file,
        #         text_contains_all=[
        #             'some text', 'another text the file must contain'
        #         ]).validate(reason)


    filename_nok_msg = 'Files must be of type ".zip", ".tar.bz2" and contain "Collection" in filename.'

    return reason_response(reason, valid_fname, valid_contents, filename_nok_msg)

"""


import os
import requests
from ..utils import RedisService, save_file
from ..quota import Quota
from licenseware.utils.log_config import log
from typing import List, Callable
from licenseware.decorators.auth_decorators import authenticated_machine
from ..utils.validators import validate_event
from licenseware.dramatiq_handler.redis_broker import broker




def reason_response(reason, valid_fname, valid_contents, filename_nok_msg='Filename is not valid.'):
    """
        :reason         - bool affects response if True will be in dict format else bool
        :valid_fname    - the response from validate_filename function from file_validators
        :valid_contents - the response from GeneralValidator.validate()
    """

    # log.warning(f"reason:{reason}, valid_fname:{valid_fname}, valid_contents:{valid_contents}")

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



class Uploader(Quota):

    """
        This library is used to register/store information about files 
        that will be uploaded and processed.

        Use case:
        ```py

        UniqueName = Uploader(
            app_id="name-service",
            upload_name="Short description",
            uploader_id="UniqueName",
            accepted_file_types=['.zip', '.tar', '.csv'],
            description="Long description",
            upload_url="/UniqueName/files",
            upload_validation_url='/UniqueName/validation',
            validation_function=valid_xxx_files, #function that validates filname and contents
            quota_collection_name=None, # if not specified will be computed from app_id (check code)
            unit_type=None, # if not specified uploader_id will be taken (this will be also the event_type for redis stream)
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
        app_id: str,
        upload_name: str,
        uploader_id: str,
        accepted_file_types: List[str],
        description: str,
        validation_function: Callable,
        # Optional parameters
        upload_url: str = None,
        upload_validation_url: str = None,
        status_check_url: str = None,
        quota_validation_url: str = None,
        history_url: str = None,
        quota_collection_name: str = None,
        unit_type: str = None,
        status: str = "idle",
        icon: str = "default.png",
        flags: list = []
    ):

        self.app_id = app_id
        self.upload_name = upload_name
        self.uploader_id = uploader_id
        self.accepted_file_types = accepted_file_types
        self.description = description
        
        self.upload_url = upload_url or f"/{uploader_id}/files"
        self.upload_validation_url = upload_validation_url or f"/{uploader_id}/validation"
        self.quota_validation_url = quota_validation_url or f"/quota/{uploader_id}"
        self.status_check_url = status_check_url or f"/{uploader_id}/status"
        self.history_url = history_url or f"/{uploader_id}/history"
        
        self.status = status
        self.icon = icon
        self.validation_function = validation_function
        self.flags = flags
        
        self.quota_collection_name = (
            quota_collection_name or str(app_id).split("-")[0].upper() + "Utilization"
        )
        self.unit_type = unit_type or self.uploader_id

        super().__init__(
            collection = self.quota_collection_name, _unit_type = self.unit_type
        )

        self.base_url = os.getenv("APP_BASE_PATH") + os.getenv("APP_URL_PREFIX") + '/uploads'
        self.registration_url = f'{os.getenv("REGISTRY_SERVICE_URL")}/uploaders'
        self.auth_token = os.getenv('AUTH_TOKEN')

        if 'local' in os.getenv("ENVIRONMENT", ""):
            self.app_id = os.getenv("APP_ID", app_id)
            self.uploader_id = f'{os.getenv("PERSONAL_PREFIX", "local")}-{uploader_id}'

    @authenticated_machine
    def register_uploader(self):

        if not self.auth_token:
            log.warning('Uploader not registered, no AUTH_TOKEN available')
            return {
                "status": "fail", 
                "message": "Uploader not registered, no AUTH_TOKEN available" 
            }, 403


        payload = {
            'data': [{
                "app_id": self.app_id,
                "upload_name": self.upload_name,
                "upload_id": self.uploader_id, #TODO Field to be later renamed to uploader_id
                "accepted_file_types": self.accepted_file_types,
                "description": self.description,
                "flags": self.flags,
                "upload_url": self.base_url + self.upload_url,
                "upload_validation_url": self.base_url + self.upload_validation_url,
                "quota_validation_url": self.base_url + self.quota_validation_url,
                "status_check_url": self.base_url + self.status_check_url,
                "history_url": self.base_url + self.history_url,
                "status": self.status,
                "icon": self.icon,
            }]
        }

        log.info(payload)
        
        headers = {"Authorization": self.auth_token}
        registration = requests.post(url=self.registration_url, json=payload, headers=headers)

        log.info(registration.content)

        if registration.status_code == 200:
            return {
                "status": "success",
                "message": "Uploader register successfully"
            }, 200

        else:
            log.warning("Could not register uploader")
            return {
                "status": "fail",
                "message": "Could not register uploader"
            }, 400

    @authenticated_machine
    def notify_registry(self, tenant_id, status):

        headers = {"Authorization": os.getenv('AUTH_TOKEN')}
        payload = {
            'data': [
                {
                    'tenant_id': tenant_id,
                    'upload_id': self.uploader_id, #to be changed later to uploader_id
                    'status': status,
                    'app_id': self.app_id
                }
            ]}
        notification_sent = requests.post(
            url=self.registration_url + '/status',
            headers=headers,
            json=payload
        )
        if notification_sent.status_code == 200:
            log.info("Notification registry service success!")
            return {"status": "success", "message": payload}, 200
        else:
            log.warning("Notification registry service failed!")
            return {"status": "fail", "message": payload}, 500



    def validate_filenames(self, request_obj):
        """
            Validate filenames from flask request.
        """

        msg, status = self._filenames_response(request_obj)
        
        if status != 200:
            
            qmsg, qstatus = self.check_quota(
                tenant_id = request_obj.headers.get("TenantId"), 
                unit_type = self.unit_type, 
                number_of_units = msg['units']
            )

            if qstatus != 200: 
                msg['status'] = qmsg['status'] #check_quota status has priority 
                return dict(msg, **qmsg), qstatus

        return msg, status


    def upload_files(self, request_obj):
        """ 
            Upload files from request.
        """
        
        msg, status = self._upload_response(request_obj, event_type=self.uploader_id)
        
        tenant_id = request_obj.headers.get("TenantId")

        if status == 200:
            qmsg, qstatus = self.update_quota(
                tenant_id = tenant_id, 
                unit_type = self.unit_type, 
                number_of_units = msg['units']
            )

            if qstatus != 200: 
                qmsg['status'] = msg['status'] #probabily quota initilized but files check failed
                return dict(msg, **qmsg), qstatus


        self.notify_registry(tenant_id, 'running')
        
        return msg, status

           

    def _filenames_response(self, request_obj, filename_ok_msg='Filename is valid.', filename_nok_msg='Filename is not valid.'):

        filenames = request_obj.json

        if not isinstance(filenames, list) and filenames:
            return {'status': 'fail', 'message': 'Must be a list of filenames.'}, 400

        validation, accepted_files = [], []
        for filename in filenames:
            status, message = 'fail', filename_nok_msg
            if self.validation_function(filename):
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
            res = self.validation_function(file, reason=True)
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



        event = {
            "tenant_id": request_obj.headers.get("TenantId"),
            "files": ",".join(saved_files),
            "event_type": event_type
        }
        
        validate_event(event)
        broker.actors[event_type].send(event)
        
        # DramatiqEvent.send(event)
        # RedisService.send_stream_event({
        #     "tenant_id": request_obj.headers.get("TenantId"),
        #     "files": ",".join(saved_files),
        #     "event_type": event_type
        # })

        return {"status": "success", "message": "files uploaded successfuly", 
            "units": len(saved_files), 
            "validation": validation
        }, 200



