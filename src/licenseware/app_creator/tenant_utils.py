import datetime
import licenseware.mongodata as m
from licenseware.serializer.app_utilization import AppUtilizationSchema
from licenseware.utils.log_config import log
from licenseware.utils.urls import APP_ID


class TenantUtils:

    def __init__(
        self,
        app_id: str = None,
        data_collection_name: str = None,
        utilization_collection_name: str = None,
        analysis_collection_name: str = None,
    ):

        self.app_id = app_id or APP_ID
        app_prefix = str(self.app_id).split('-')[0].upper()
        # services names should be named like "XXX-name" where XXX it's a unique acronym

        self.data_collection_name = data_collection_name or app_prefix + "Data"
        self.utilization_collection_name = utilization_collection_name or app_prefix + "Utilization"
        self.analysis_collection_name = analysis_collection_name or app_prefix + "AnalysisStats"

    # Processing status

    def _get_timed_out_files(self, tenant_id):

        time_out_time = datetime.datetime.utcnow() - datetime.timedelta(minutes=5)
        start_time = datetime.datetime.utcnow() - datetime.timedelta(days=360)

        query = {
            'tenant_id': tenant_id,
            'status': 'Running',
            'updated_at': {'$gt': start_time.isoformat(), '$lt': time_out_time.isoformat()}
        }

        return m.fetch(match=query, collection=self.analysis_collection_name)

    def _close_timed_out(self, timed_out_file):

        timed_out_file["status"] = "Error"

        return m.update(
            schema=AppUtilizationSchema,
            match=timed_out_file,
            new_data=timed_out_file,
            collection=self.analysis_collection_name
        )

    def get_processing_status(self, tenant_id):

        [self._close_timed_out(f)
         for f in self._get_timed_out_files(tenant_id)]

        query = {'tenant_id': tenant_id, 'status': 'Running'}
        results = m.fetch(
            match=query, collection=self.analysis_collection_name)
        log.info(results)

        if results:
            return {'status': 'Running'}, 200
        return {'status': 'Idle'}, 200

    def get_uploader_status(self, tenant_id, uploader_id):
        [self._close_timed_out(f)
         for f in self._get_timed_out_files(tenant_id)]
        query = {'tenant_id': tenant_id,
                 'status': 'Running', 'file_type': uploader_id}
        results = m.fetch(
            match=query, collection=self.analysis_collection_name)
        log.info(results)

        if results:
            return {'status': 'Running'}, 200
        return {'status': 'Idle'}, 200

    # Activated tenants and tenants with data

    def clear_tenant_data(self, tenant_id):

        res = m.delete(
            match={'tenant_id': tenant_id},
            collection=self.data_collection_name
        )

        log.info(f"tenant data deleted: {res}")

    def get_activated_tenants(self):
        tenants_list = m.fetch(
            match='tenant_id', collection=self.utilization_collection_name)
        log.info(f"Activated_tenants: {tenants_list}")
        return tenants_list

    def get_last_update_dates(self):
        pipeline = [
            {
                '$group': {
                    '_id': {
                        'tenant_id': '$tenant_id'
                    },
                    'last_update_date': {
                        '$max': '$updated_at'
                    }
                }
            }, {
                '$project': {
                    '_id': 0,
                    'tenant_id': '$_id.tenant_id',
                    'last_update_date': '$last_update_date'
                }
            }
        ]

        last_update_dates = m.aggregate(
            pipeline, collection=self.data_collection_name)

        if not last_update_dates:
            log.info("Could not get last update dates")

        return last_update_dates

    def get_tenants_with_data(self):

        enabled_tenants = self.get_last_update_dates()

        if enabled_tenants:
            enabled_tenants = [{
                "tenant_id": tenant["tenant_id"],
                "last_update_date": tenant["last_update_date"]
            } for tenant in enabled_tenants]

        log.info(f"enabled_tenants: {enabled_tenants}")
        return enabled_tenants
