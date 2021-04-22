import pytest
from assertpy import assert_that
from lware.registry import Uploader
import os 


os.environ['APP_BASE_PATH'] = "localhost"
os.environ['APP_URL_PREFIX'] = "/path"
os.environ['AUTH_TOKEN'] = 'AUTH_TOKEN'



def test_register_uploader():

    UniqueName = Uploader(
        app_id="name-service",
        upload_name="Short description",
        upload_id="UniqueName",
        description="Long description",
        upload_url="/UniqueName/files",
        upload_validation_url='/UniqueName/validation',
        quota_validation_url='/quota/UniqueName',
        status_check_url='/UniqueName/status',
        history_url='/UniqueName/history',
        validate_upload_function=lambda d: d,
        validate_filename_function=lambda d: d
        
        #Unfortunately works only on stack
        # base_url="http://localhost:5003/ifmp",
        # registration_url="http://localhost:2818/registry-service",
        # auth_token="",
    )

    response, status_code = UniqueName.register_uploader()

    assert_that(status_code).is_equal_to(200)

