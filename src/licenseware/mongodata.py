"""

Abstraction and validation of inserted data in mongodb


import licenseware.mongodata as m
or
from licenseware import mongodata as m

Available functions:
- get_collection
- insert
- fetch
- update
- delete
- aggregate

Needs the following environment variables:
- MONGO_DATABASE_NAME
- MONGO_CONNECTION_STRING
- MONGO_COLLECTION_NAME (optional)

"""

import os
from re import I
from typing import List
from uuid import UUID
from pymongo import MongoClient
from pymongo.collection import Collection
from bson.json_util import dumps
from bson.objectid import ObjectId
import json
from .decorators import failsafe
from .utils.log_config import log



#Utils

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

def _parse_oid(oid):
    if isinstance(oid, ObjectId):
        return json.loads(dumps(oid))['$oid']
    return oid

def _parse_doc(doc):
    if not isinstance(doc, dict): return doc
    if not "_id" in doc: return doc

    return dict(doc, **{"_id": _parse_oid(doc["_id"])})



def _parse_match(match):
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



def _create_del_dups_pipeline(collection_name: str, fields:list) -> List[dict]:
    """
        Remove duplicates aggregation pipeline generated from fields which contain list of dicts.

        $addToSet + $each works on removing duplicates only with simple lists like: [1,2,2,3] or ['val1', 'val2', 'val2']
        $addToSet + $each can't remove duplicates from list of objects: [{5:5}, {3:4}, {5:5}]
    """
    
    #TODO if fields order is different than it's considered a different object 
    # that's way on insert and update we added `sorted_data` function
    # in the $reduce we need to include $cond '_id' if present (that way we can get rid of _get_unique_ids_pipeline)

    set_stage = {'$set': {}}
    for field_name in fields:
        field_nodups = {
            field_name: {
                '$setUnion': {
                    '$reduce': {
                    'input': '$'+field_name,
                    'initialValue': '$'+field_name,
                    'in': { '$setUnion': ["$$value", ["$$this"]] }
                }}
                }
            }
        
        set_stage['$set'].update(field_nodups)
        
    merge_stage = {
        '$merge': {
            'into': collection_name
        }
    }

    pipeline_remove_dups = [set_stage, merge_stage] 
    
    # print(pipeline_remove_dups)

    return pipeline_remove_dups



def _get_fields_with_listof_dicts(new_data: dict) -> List[str]:
    fields_with_lists = [k for k in new_data if isinstance(new_data[k], list) and new_data[k]]
    fields_with_listof_dicts = [k for k in fields_with_lists if isinstance(new_data[k][0], dict)]
    return fields_with_listof_dicts



def _append_query(dict_: dict) -> dict:
    """ 
        Force append to mongo document 
    """
    
    dict_.pop("_id", None)
    
    q = {'$set': {}, '$addToSet': {}}
    for k in dict_:
        
        if isinstance(dict_[k], str):
            q['$set'].update({k:dict_[k]})
            
        if isinstance(dict_[k], dict):
            for key in dict_[k]:
                key_ = ".".join([k, key]) # files.status
                q['$set'].update({key_:dict_[k][key]})
                
        if isinstance(dict_[k], list): 
            q['$addToSet'].update({k:{}})
            q['$addToSet'][k].update({ "$each": dict_[k]})
     
    if not q['$addToSet']: del q['$addToSet'] 
    if not q['$set']: del q['$set'] 

    # print(q)

    return q or dict_



def _remove_duplicates_from_list_of_objects(match:dict, data: dict, collection: str) -> None:
    """
        Remove duplicates from fields which contain list of objects
    """

    fields = _get_fields_with_listof_dicts(data)
    if fields:
        del_dups_pipeline = _create_del_dups_pipeline(collection, fields)
        del_dups_pipeline = [{'$match':match}] + del_dups_pipeline
        # print(del_dups_pipeline)
        aggregate(pipeline=del_dups_pipeline, collection=collection)
    
    

def sorted_data(data):   
    """
        Hack for _remove_duplicates_from_list_of_objects to work
        $setUnion considers object with different fields order by same data as different..
    """
    sort_dict = lambda data: {k:data[k] for k in sorted(data)}
    
    if isinstance(data, dict):
        data = sort_dict(data)

    if isinstance(data, list) and len(data) > 0:
        if isinstance(data[0], dict):
            data = [sort_dict(d) for d in data]
    
    return data




#Mongo

default_db = os.getenv("MONGO_DB_NAME") or os.getenv("MONGO_DATABASE_NAME") or "db"
default_collection = os.getenv("MONGO_COLLECTION_NAME") or "Data"
mongo_connection = MongoClient(os.getenv("MONGO_CONNECTION_STRING"))


@failsafe
def get_collection(collection, db_name=None):
    """
        Gets the collection on which mongo CRUD operations can be performed

        If something fails will return a string with the error message.
    """
    
    collection = collection or default_collection
    db_name = db_name or default_db

    # print(db_name, collection, os.getenv("MONGO_CONNECTION_STRING"), mongo_connection)

    if not all([db_name, collection, mongo_connection]) :
        raise Exception("Can't create connection to mongo.")

    collection = mongo_connection[db_name][collection]
    
    return collection


@failsafe
def insert(schema, collection, data, db_name=None):
    """
        Insert validated documents in database.

        :schema     - Marshmallow schema class used to validate `data`
        :collection - collection name, schema name will be taken if not present
        :data       - data in dict or list of dicts format
        :db_name    - specify other db if needed, by default is MONGO_DATABASE_NAME from .env

        returns a list of ids inserted in the database in the order they were added
        If something fails will return a string with the error message.
    """

    collection = get_collection(collection, db_name)
    if not isinstance(collection, Collection): 
        return collection 

    data = validate_data(schema, data)
    if isinstance(data, str): return data
    data = sorted_data(data)


    if isinstance(data, dict):
        inserted_id = _parse_oid(collection.insert_one(data).inserted_id)
        return [inserted_id]

    if isinstance(data, list):
        inserted_ids = collection.insert_many(data).inserted_ids
        return [_parse_oid(oid) for oid in inserted_ids]

    raise Exception(f"Can't interpret validated data: {data}")




@failsafe
def fetch(match, collection, as_list=True, db_name=None):
    """
        Get data from mongo, based on match dict or string id.
        
        :match      - _id as string (will return a dict)
                    - mongo dict filter (will return a list of results)
                    - field_name as string (will return distinct values for that field)

        :collection - collection name
        :as_list    - set as_list to false to get a generator
        :db_name    - specify other db if needed by default is MONGO_DATABASE_NAME from .env
        
        If something fails will return a string with the error message.

    """
    
    match = _parse_match(match)

    collection = get_collection(collection, db_name)
    if not isinstance(collection, Collection): return collection 

    if match['_id']:
        found_docs = collection.find(match['_id'])
        doc = []
        if found_docs: doc = list(found_docs)[0]
        if match['oid']: doc = _parse_doc(doc)
        return doc

    if match['distinct_key']: 
        found_docs = collection.distinct(match['distinct_key'])
    elif match['query_tuple']:
        found_docs = collection.find(*match['query_tuple'])
    else:
        found_docs = collection.find(match['query'])

    if as_list: 
        return [_parse_doc(doc) for doc in found_docs]
        
    return (_parse_doc(doc) for doc in found_docs)    
        


@failsafe
def aggregate(pipeline, collection, as_list=True, db_name=None):
    """
        Fetch documents based on pipeline queries.
        https://docs.mongodb.com/manual/reference/operator/aggregation-pipeline/
        
        :pipeline   - list of query stages
        :collection - collection name
        :as_list    - set as_list to false to get a generator
        :db_name    - specify other db if needed by default is MONGO_DATABASE_NAME from .env
                
        If something fails will return a string with the error message.

    """

    collection = get_collection(collection, db_name)
    if not isinstance(collection, Collection): return collection 

    found_docs = collection.aggregate(pipeline, allowDiskUse=True)

    if as_list: return [_parse_doc(doc) for doc in found_docs]
        
    return (_parse_doc(doc) for doc in found_docs)    
        



@failsafe
def update(schema, match, new_data, collection, append=False, db_name=None):
    """
        Update documents based on match query.
        
        :schema      - Marshmallow schema class
        :match       - id as string or dict filter query
        :new_data    - data dict which needs to be updated
        :collection  - collection name
        :append      - if true will APPEND new data to existing fields, if false will SET new data to fields  
        :db_name     - specify other db if needed by default is MONGO_DATABASE_NAME from .env
        
        returns number of modified documents

        If something fails will return a string with the error message.

    """

    match = _parse_match(match)
    match = match['query'] or match['_id'] 
    if not match:
        match = match['_id'] = match['distinct_key']
    
    collection_name = collection
    collection = get_collection(collection, db_name)
    if not isinstance(collection, Collection): return collection 

    new_data = validate_data(schema, new_data)
    if isinstance(new_data, str): return new_data
    new_data = sorted_data(new_data)

    _filter = {"_id": match["_id"]} if "_id" in match else match
    updated_docs_nbr = collection.update_many(
        filter=_filter,
        update=_append_query(new_data) if append else {"$set": new_data},
        upsert=True
    ).modified_count

    if isinstance(updated_docs_nbr, str): return updated_docs_nbr

    if append:
        _remove_duplicates_from_list_of_objects(
            match = _filter, 
            data = new_data, 
            collection = collection_name
        )
        
    return updated_docs_nbr




@failsafe
def delete(match, collection, db_name=None):
    """

        Delete documents based on match query.

        :match       - id as string or dict filter query,           
        :collection  - collection name
        :db_name     - specify other db if needed by default is MONGO_DATABASE_NAME from .env
        
        returns number of deleted documents
        
        If something fails will return a string with the error message.

    """
    match = _parse_match(match)

    col = get_collection(collection, db_name)
    if not isinstance(col, Collection): return col 

    deleted_docs_nbr = col.delete_many(
        filter=match['query'] or match['_id'],
    ).deleted_count
    
    return deleted_docs_nbr


@failsafe
def delete_collection(collection, db_name=None):
    """
        Delete a collection from the database.
    """

    col = get_collection(collection, db_name)
    if not isinstance(col, Collection): return col 

    res = col.drop()
    return 1 if res is None else 0

