"""

Each cron job should be a function without paramters
Once defined add it to `cron_jobs_list` list

"""

from licenseware.app_creator.tenant_utils import TenantUtils


def set_status_failed_for_timed_out_files():
    # using low_memory just in case we have tons of data
    TenantUtils().close_timed_out_files(low_memory=True)







cron_jobs_list = [
    set_status_failed_for_timed_out_files
]