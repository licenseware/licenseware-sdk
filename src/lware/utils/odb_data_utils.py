import logging
from lware.service.data_management_service import DataManagement as dm


def get_enabled_tenants():
    _filter = {
        'doc_type': 'database',
    } 
    tenants, status = dm(collection="data").return_distinct_values(key="tenant_id", _filter=_filter)
    if tenants: return tenants
    logging.warning("No tenants with data")
    return []
    

def get_activated_tenants():
    tenants, status = dm(collection="ODBUtilization").return_distinct_values(key="tenant_id")
    if tenants: return tenants
    logging.warning("No tenants activated")
    return []


    
def get_last_update_dates():
    pipeline = [
        {
            '$match': {
                'doc_type': 'database'
            }
        }, {
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
    last_update_dates = dm(collection="data").get_with_aggregation(pipeline)
    if last_update_dates[1] == 200:
        return last_update_dates[0]
    logging.warning("Could not get last update dates")
    return []



def get_tenants_with_data():
    
    enabled_tenants = get_last_update_dates()

    if enabled_tenants:
        enabled_tenants = [{
            "tenant_id": tenant["tenant_id"], 
            "last_update_date": tenant["last_update_date"]
        } for tenant in enabled_tenants]

    return enabled_tenants
