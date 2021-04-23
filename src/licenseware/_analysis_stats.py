"""
Not integrated
"""

import datetime
import uuid
import logging

from .data_management import DataManagement as dm
from .serializer import AnalysisStatsSchema
import mongodata as m


def get_timedout_databases(tenant_id):
    time_out_time = datetime.datetime.utcnow() - datetime.timedelta(minutes=15)
    start_time = datetime.datetime.utcnow() - datetime.timedelta(days=360)

    _filter = {'tenant_id': tenant_id,  'files.status': { "$eq": 'Running' }, 'doc_type': 'stats',
               'updated_at': {'$gt': start_time.isoformat(), '$lt': time_out_time.isoformat()}}
    return dm(AnalysisStatsSchema, collection="DBAnalysisStats").get_all(_filter)

def close_timed_out(timed_out_db):
    timed_out_db["status"] = "Error"
    return dm(AnalysisStatsSchema, collection="DBAnalysisStats").replace_one(timed_out_db)


class AnalysisStatsService:

    @staticmethod
    def update_one(json_data):
        print(json_data)
        json_data['updated_at'] = datetime.datetime.utcnow().isoformat()
        json_data['_id'] = str(uuid.uuid4())
        print(json_data['updated_at'])
        return dm(AnalysisStatsSchema, collection="DBAnalysisStats").update_one(json_data, _filter={'tenant_id': json_data['tenant_id'],
                                                                      'database_id': json_data['database_id']})

    @staticmethod
    def return_all(tenant_id):
        _filter = {'tenant_id': tenant_id, 'doc_type': 'stats'}
        return dm(AnalysisStatsSchema, collection="DBAnalysisStats").get_all(_filter)

    @staticmethod
    def return_status(tenant_id, file_type):
        timed_out = get_timedout_databases(tenant_id)
        if timed_out[1] == 200:
            for db in timed_out[0]:
                close_timed_out(db)

        query = {
            'tenant_id': tenant_id, 
            'file_type': file_type, 
            'files.status': { "$eq": 'Running' }
        }
        
        results = m.fetch(
            collection="DBAnalysisStats", match=query, as_list=True
        )

        # logging.warning("--------- return_status DBAnalysisStats")
        # logging.warning(results)

        if results: 
            return {'status': 'Running'}, 200

        return {'status': 'Idle'}, 200
        

    @staticmethod
    def add_stats_from_db_event(json_data):
        try:
            stats = {
                '_id': str(uuid.uuid4()),
                'tenant_id': json_data['tenant_id'],
                'database_id': json_data['_id'],
                'status': 'Running',
                'updated_at': datetime.datetime.utcnow().isoformat(),
                'doc_type': 'stats',
                'file_type': json_data['event_type']
            }
            print(stats)
            return dm(AnalysisStatsSchema, collection="DBAnalysisStats").update_one(stats, _filter={'tenant_id': stats['tenant_id'],
                                                                      'database_id': stats['database_id']})
        except Exception as e:
            print(e)
            return None

