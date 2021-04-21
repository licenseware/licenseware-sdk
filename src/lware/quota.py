"""
Use case:

from lware.quota import Quota

q = Quota(collection="CollectionName")

q.init_quota(tenant_id, unit_type)


"""

import datetime
import os
import sys
import uuid
import dateutil.parser as dateparser
import lware.mongodata as m
from .schemas.app_utilization import AppUtilizationSchema


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


class Quota:

    def __init__(self, collection=None, schema=None):
        self.schema = schema or AppUtilizationSchema
        self.collection = collection


    def init_quota(self, tenant_id, unit_type):

        results = m.fetch(
            match={'tenant_id': tenant_id, 'unit_type': unit_type},
            collection=self.collection
        )

        if results:
            return {'status': 'fail', 'message': 'App already installed'}, 400

        init_data = {
            "_id": str(uuid.uuid4()),
            "tenant_id": tenant_id,
            "unit_type": unit_type,
            "monthly_quota": QUOTA[unit_type],
            "monthly_quota_consumed": 0,
            "quota_reset_date": get_quota_reset_date()
        }

        inserted_ids = m.insert(
            schema=self.schema, data=init_data, collection=self.collection
        )

        if len(inserted_ids) == 1:
            return {'status': 'success', 'message': 'Quota initialized'}, 200
        
        return {'status': 'fail', 'message': 'Quota failed to initialize'}, 500



    def update_quota(self, tenant_id, unit_type, number_of_units):

        current_utilization = m.fetch(
            match={'tenant_id': tenant_id, 'unit_type': unit_type},
            collection=self.collection
        )

        if current_utilization:
            new_utilization = current_utilization[0]
            new_utilization['monthly_quota_consumed'] += number_of_units
            
            updated_docs = m.update(
                schema=self.schema,
                match=current_utilization[0],
                new_data=new_utilization,
                collection=self.collection
            )

            if updated_docs == 1:
                return {'status': 'success', 'message': 'Quota updated'}, 200
            else:
                return {'status': 'fail', 'message': 'Quota failed to be updated'}, 500

        else:
            new_user_status, response = self.init_quota(tenant_id, unit_type)
            if response == 200:
                retry_update = self.update_quota(tenant_id, unit_type, number_of_units)
                return retry_update
            else:
                return new_user_status, response


    def check_quota(self, tenant_id, unit_type, number_of_units=0):
        
        query = {'tenant_id': tenant_id, 'unit_type': unit_type}

        results = m.fetch(query, self.collection)

        if not results:
            new_user_response, status = self.init_quota(tenant_id, unit_type)
            if status == 200:
                results = m.fetch(query, self.collection)
                if results: quota = results[0]
            else:
                return new_user_response, status
        else:
            quota = results[0]


        # Reset quota if needed 
        quota_reset_date = dateparser.parse(quota['quota_reset_date'])
        current_date = datetime.datetime.utcnow()
        if quota_reset_date < current_date:
            quota['quota_reset_date'] = get_quota_reset_date()
            quota['monthly_quota_consumed'] = 0
            m.update(results[0], quota, self.collection)
            # Recall check_quota method with the new reseted date and quota
            self.check_quota(tenant_id, unit_type, number_of_units)

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
