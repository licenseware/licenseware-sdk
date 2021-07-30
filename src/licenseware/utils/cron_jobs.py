"""

Each cron job should be a function without paramters
Once defined add it to `cron_jobs_list` list

"""

from .file_timeouts import FileTimeout




def set_status_failed_for_timed_out_files():
    # using low_memory just in case we have tons of data
    FileTimeout(low_memory=True).close_timed_out_files()





cron_jobs_list = [
    set_status_failed_for_timed_out_files
]