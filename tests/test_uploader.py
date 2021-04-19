import unittest
from .uploader import Uploader


class TestUploader(unittest.TestCase):

    def test_register_uploader(self):

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
            #Unfortunately works only on stack
            # base_url="http://localhost:5003/ifmp",
            # registration_url="http://localhost:2818/registry-service",
            # auth_token="",
        )

        response, status_code = UniqueName.register_uploader()

        self.assertEqual(status_code, 200)
    
    




if __name__ == '__main__':
    unittest.main()