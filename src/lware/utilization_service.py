import datetime
import logging
import os
import sys
import uuid
import dateutil.parser as parser
from .mongodata import MongoData as m


QUOTA = {
    #IFMP
    "cpuq": 10,  # Databases
    "rv_tools": 1,  # Files
    "lms_detail": 1,  # Files
    
    #ODB
    "review_lite": 16, # Databases
    "lms_options": 1, # Files
}


if os.getenv('DEBUG') == 'true':
    QUOTA = dict(
        zip(QUOTA.keys(), [sys.maxsize]*len(QUOTA.keys()))
    )

    
# Utils

def get_quota_reset_date():
    quota_reset_date = datetime.datetime.utcnow() + datetime.timedelta(days=30)
    return quota_reset_date.isoformat()


class UtilizationService:

    def __init__(self, collection="Quota"):
        self.collection = collection
        # self.dm = dm_service(_schema=AppUtilizationSchema, collection="IFMPUtilization")



    @classmethod
    def init_quota(cls, tenant_id, unit_type):
        c = cls()  # needs initialization
        _filter = {'tenant_id': tenant_id, 'unit_type': unit_type}
        _, status_code = c.dm.get_one_with_filter(_filter)
        if status_code == 404:

            init_data = {
                "_id": str(uuid.uuid4()),
                "tenant_id": tenant_id,
                "unit_type": unit_type,
                "monthly_quota": QUOTA[unit_type],
                "monthly_quota_consumed": 0,
                "quota_reset_date": get_quota_reset_date()
            }

            # logging.warning(init_data)
            _, status_code = c.dm.insert_data(init_data)

            if status_code == 202:
                return {'status': 'success', 'message': 'Quota initialized'}, 200
            else:
                return {'status': 'fail', 'message': 'Quota failed to initialize'}, 500
        else:
            return {'status': 'fail', 'message': 'App already installed'}, 400

    @classmethod
    def update_quota(cls, tenant_id, unit_type, number_of_units):
        c = cls()

        _filter = {'tenant_id': tenant_id, 'unit_type': unit_type}
        current_utilization = c.dm.get_one_with_filter(_filter)

        if current_utilization[1] == 200:

            new_utilization = current_utilization[0]
            new_utilization['monthly_quota_consumed'] += number_of_units
            _, status_code = c.dm.update_one(new_utilization)

            if status_code in [200, 201, 202]:
                return {'status': 'success', 'message': 'Quota updated'}, 200
            else:
                return {'status': 'fail', 'message': 'Quota failed to be updated'}, 500

        else:
            new_user_status, response = cls.init_quota(tenant_id, unit_type)
            if response == 200:
                retry_update = cls.update_quota(tenant_id, unit_type, number_of_units)
                return retry_update
            else:
                return new_user_status, response

    @classmethod
    def check_quota(cls, tenant_id, unit_type, number_of_units=0):
        c = cls()
        _filter = {'tenant_id': tenant_id, 'unit_type': unit_type}
        quota, status_code = c.dm.get_one_with_filter(_filter)

        if status_code != 200:
            new_user_response, status = c.init_quota(tenant_id, unit_type)
            if status in [200, 201, 202]:
                quota, status_code = c.dm.get_one_with_filter(_filter)
            else:
                return new_user_response, status

        logging.warning('quota')
        logging.warning(quota)

        # Reset quota if needed 
        quota_reset_date = parser.parse(quota['quota_reset_date'])
        current_date = datetime.datetime.utcnow()
        if quota_reset_date < current_date:
            quota['quota_reset_date'] = get_quota_reset_date()
            quota['monthly_quota_consumed'] = 0
            c.dm.update_one(quota)
            # Recall check_quota method with the new reseted date and quota
            UtilizationService.check_quota(tenant_id, unit_type, number_of_units)

        if quota['monthly_quota_consumed'] <= quota['monthly_quota'] + number_of_units:
            return {
                       'status': 'success',
                       'message': 'Utilization within monthly quota'
                   }, 200
        else:
            return {
                       'status': 'fail',
                       'message': 'Monthly quota exceeded'
                   }, 402
