from uuid import UUID
from bson.json_util import dumps
from bson.objectid import ObjectId
import json
from ..decorators import failsafe
from ..utils import log, log_dict



@failsafe
def validate_data(schema, data): 
    """
        Using Marshmallow schema class to validate data (dict or list of dicts) 
    """ 

    if isinstance(data, dict):
        data = schema().load(data)

    if isinstance(data, list):
        data = schema(many=True).load(data)

    return data


def valid_uuid(uuid_string):
    try:
        UUID(uuid_string)
        return True
    except ValueError:
        return False

def valid_object_id(oid_string):
    try:
        ObjectId(oid_string)
        return True
    except:
        return False

def parse_oid(oid):
    if isinstance(oid, ObjectId):
        return json.loads(dumps(oid))['$oid']
    return oid


def parse_doc(doc):
    if not isinstance(doc, dict): return doc
    if not "_id" in doc: return doc

    return dict(doc, **{"_id": parse_oid(doc["_id"])})



def parse_match(match):
    # query_tuple - select only fields 
    # distinct_key - select distinct fields

    categ = {
        '_id': None,
        'oid': None, 
        'uid': None, 
        'distinct_key': None,  
        'query_tuple': None, 
        'query': None
    }

    if isinstance(match, dict):
        
        if '_id' in match:
            if valid_object_id(match['_id']):
                match['_id'] = ObjectId(match['_id'])
                
        categ['query'] = match
        
    elif isinstance(match, str): 
        if valid_uuid(match): 
            match = {"_id": match}
            categ['uid'] = match
        elif valid_object_id(match):
            match = {"_id": ObjectId(match)}
            categ['oid'] = match
        else:
            categ['distinct_key'] = match

        categ['_id'] = categ['uid'] or categ['oid']

    elif (isinstance(match, tuple) or isinstance(match, list)) and len(match) == 2:
        categ['query_tuple'] = match
    else:
        raise ValueError("Can't parse match query")

    return categ 



# sort_dict = lambda data: {k:data[k] for k in sorted(data)}
