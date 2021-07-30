"""

Each cron job should be a function without paramters
Once defined add it to `cron_jobs_list` list

"""

from .urls import APP_ID
from .file_timeouts import FileTimeout
from .update_registry import update_registry
from .log_config import log



def set_status_failed_for_timed_out_files():
    
    # TODO normalize names (same meaning for all):
    # file_type, event_type, uploader_id, upload_id 
    
    # TODO App id we just need the first chunk before `-`:
    # 'ifmp-service', 'ifmp-worker' (just ifmp), 'mdm-service', 'mdm-worker' (just mdm)
    
    # Using low_memory just in case we have tons of data
    ft = FileTimeout(low_memory=True)
    
    for analysis_data in ft.get_timed_out_files():
        
        ft.close_timed_out(analysis_data)
        
        tenant_id = analysis_data.get('tenant_id')
        upload_id = analysis_data.get('file_type')
        
        if not all([tenant_id, upload_id]):
            log.warning("File analysis data didn't contain `tenant_id` and/or `file_type`!")
            continue
        
        update_registry({
            'tenant_id': tenant_id, 
            'upload_id': upload_id,
            'status': 'idle', # sending idle to force registry to send idle status on front end
            'app_id': APP_ID.replace('worker', 'service')   
        })
        
        





cron_jobs_list = [
    set_status_failed_for_timed_out_files
]