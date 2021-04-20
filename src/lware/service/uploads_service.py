import logging, traceback
import os, re, uuid

from werkzeug.utils import secure_filename
from ..utils.redis_service import RedisService
# from ..file_validators import GeneralValidator, validate_filename


class UploadsService:

    @staticmethod
    def receive_files_cpuq(_request):

        return upload_response(
            _request, 
            valid_cpuq_file, 
            event_type="cpuq"
        )
        
    @staticmethod
    def receive_files_rvtools(_request):

        return upload_response(
            _request, 
            valid_rv_tools_file, 
            event_type="rv_tools"
        )
        

    @staticmethod
    def receive_files_lms_details(_request):

        return upload_response(
            _request, 
            valid_lms_detail_file, 
            event_type="lms_detail"
        )
        

    @staticmethod
    def validate_uploads_cpuq(_request):

        filename_ok_msg  = 'Filename is valid.'
        filename_nok_msg = 'Files must be of type ".txt" and contain "cpuq" in filename.'

        return filenames_response(
            _request, 
            valid_cpuq_file, 
            filename_ok_msg, 
            filename_nok_msg
        )


    @staticmethod
    def validate_uploads_rvtools(_request):

        filename_ok_msg  = 'Filename is valid.'
        filename_nok_msg = 'Files must be of type ".xls" or ".xlsx" and contain "RV" and/or "Tools" in filename.'

        return filenames_response(
            _request, 
            valid_rv_tools_file, 
            filename_ok_msg, 
            filename_nok_msg
        )


    @staticmethod
    def validate_uploads_lms_details(_request):

        filename_ok_msg  = 'Filename is valid.'
        filename_nok_msg = 'Files must be of type ".csv" and contain "_detail" in filename.'

        return filenames_response(
            _request, 
            valid_lms_detail_file, 
            filename_ok_msg, 
            filename_nok_msg
        )




def filenames_response(_request, validator_func, 
                    filename_ok_msg='Filename is valid.', 
                    filename_nok_msg='Filename is not valid.'):

    filenames = _request.json

    if not isinstance(filenames, list):
        return {'status': 'fail', 'message': 'Must be a list of filenames.'}, 400

    validation, accepted_files = [], []
    for filename in filenames:
        status, message = 'fail', filename_nok_msg
        if validator_func(filename):
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



def upload_response(_request, validator_func, event_type):

    file_objects = _request.files.getlist("files[]")
    if not isinstance(file_objects, list):
        return {"status": "fail", "message": "key needs to be files[]"}, 400
        
    saved_files, validation = [], []
    for file in file_objects:
        res = validator_func(file, reason=True)
        if res['status'] == "success":
            filename = save_file(file, _request.headers.get("TenantId"))
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
        "tenant_id": _request.headers.get("TenantId"),
        "files": ",".join(saved_files),
        "event_type": event_type
    })

    return {"status": "success", "message": "files uploaded successfuly", 
        "units": len(saved_files), 
        "validation": validation
    }, 200




def save_file(file, tenant_id):
    filename = secure_filename(file.filename)

    save_path = os.path.join(os.getenv("UPLOAD_PATH"), tenant_id)
    if not os.path.exists(save_path): os.mkdir(save_path)

    file.seek(0)  # move cursor to 0 (stream left it on last read)
    file.save(os.path.join(save_path, filename))

    logging.info(f"File saved: {filename}")

    return filename


def valid_lms_detail_file(file, reason=False):

    valid_fname, valid_contents = None, None
    
    if isinstance(file, str):
        valid_fname = validate_filename(file, ['_detail'], ['.csv'])
        valid_contents = True

    if "stream" in str(dir(file)):
        valid_fname = validate_filename(file.filename, ['_detail'], ['.csv'])
        if valid_fname:
            valid_contents = GeneralValidator(
                input_object=file,
                text_contains_all=[
                    'MACHINE_ID', 'BANNER', 'DB_NAME', 'SERVER_MANUFACTURER', 'SERVER_MODEL',
                    'OPERATING_SYSTEM', 'SOCKETS_POPULATED_PHYS', 'TOTAL_PHYSICAL_CORES', 'PROCESSOR_IDENTIFIER',
                    'PROCESSOR_SPEED', 'TOTAL_LOGICAL_CORES', 'PARTITIONING_METHOD'
                ]).validate(reason)

    filename_nok_msg = 'Files must be of type ".csv" and contain "_detail" in filename.'
    return reason_response(reason, valid_fname, valid_contents, filename_nok_msg)


def valid_rv_tools_file(file, reason=False):
    
    valid_fname, valid_contents = None, None
    
    if isinstance(file, str):
        valid_fname = validate_filename(file, ['RV', 'Tools'], ['.xls', '.xlsx'])
        valid_contents = True

    if "stream" in str(dir(file)):
        valid_fname = validate_filename(file.filename, ['RV', 'Tools'], ['.xls', '.xlsx'])
        if valid_fname:
            valid_contents = GeneralValidator(
                input_object=file,
                required_input_type="excel",
                min_rows_number=1,
                required_sheets=['tabvInfo', 'tabvCPU', 'tabvHost', 'tabvCluster'],
                required_columns=[
                    'VM', 'Host', 'OS', 'Sockets', 'CPUs', 'Model', 'CPU Model',
                    'Cluster', '# CPU', '# Cores', 'ESX Version', 'HT Active',
                    'Name', 'NumCpuThreads', 'NumCpuCores'
                ]).validate(reason)

    filename_nok_msg = 'Files must be of type ".xls" or ".xlsx" and contain "RV" and/or "Tools" in filename.'
    return reason_response(reason, valid_fname, valid_contents, filename_nok_msg)


def valid_cpuq_file(file, reason=False):
    
    valid_fname, valid_contents = None, None
    
    if isinstance(file, str):
        valid_fname = validate_filename(file, ['cpuq'], ['.txt'])
        valid_contents = True

    if "stream" in str(dir(file)):
        valid_fname = validate_filename(file.filename, ['cpuq'], ['.txt'])
        if valid_fname:
            valid_contents = GeneralValidator(input_object=file).validate(reason)


    filename_nok_msg = 'Files must be of type ".txt" and contain "cpuq" in filename.'
    return reason_response(reason, valid_fname, valid_contents, filename_nok_msg)



def reason_response(reason, valid_fname, valid_contents, filename_nok_msg='Filename is not valid.'):
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
