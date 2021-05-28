import pytest
from assertpy import assert_that
import os
from licenseware import mongodata as m
from marshmallow import Schema, fields
import uuid
import datetime as dt


# Add init file in src for tests
# You need a running mongodb instance running 
# mongo express is useful for visualizing data

MONGO_ROOT_USERNAME = 'licensewaredev'
MONGO_ROOT_PASSWORD ='license123ware'
MONGO_DATABASE_NAME='db'
MONGO_HOSTNAME= 'localhost' #for a docker environment use 'mongodb' (service name)
MONGO_PORT=27017

os.environ['MONGO_DATABASE_NAME'] = MONGO_DATABASE_NAME
os.environ['MONGO_CONNECTION_STRING'] = f"mongodb://{MONGO_ROOT_USERNAME}:{MONGO_ROOT_PASSWORD}@{MONGO_HOSTNAME}:{MONGO_PORT}"

#print(os.getenv("MONGO_DATABASE_NAME"))
#print(os.getenv("MONGO_CONNECTION_STRING"))

# #print(dir(dm))


class DummySchema(Schema):
    _id = fields.Str(required=False)
    name = fields.Str(required=True)
    files = fields.List(fields.Str, required=False)
    age = fields.Integer(required=True, error_messages={"required": "Age is required."})
    birthdate = fields.DateTime(default=dt.datetime(2017, 9, 29))



class AnotherDummySchema(Schema):
    _id = fields.Str(required=False)
    name = fields.Str(required=True)
    test_list = fields.List(fields.Raw, required=False)
    test_list2 = fields.List(fields.Raw, required=False)
    test_dict = fields.Dict(fields.Raw, required=False)
    test_list_of_dict = fields.List(fields.Dict, required=False)
    some_field = fields.Str(required=False)



# Id to be used by test funcs
id1 = str(uuid.uuid4())
existing_id = str(uuid.uuid4())


dummy_data = \
{
    # "_id": id1,
    "name": "John",
    "files": ["f1", "f2"],
    "age": 20,
    "birthdate": dt.datetime(2021, 9, 29).strftime( '%Y-%m-%d %H:%M:%S' )
}



def test_insert_one():
    
    id_list = m.insert(
        schema=DummySchema, 
        collection="testcollection", 
        data={
            "_id": id1,
            "name": "John Show",
            "files": ["f1", "f2"],
            "age": "20",
            "birthdate": dt.datetime(2021, 9, 29).strftime( '%Y-%m-%d %H:%M:%S' )
        }
    )
    
    assert_that(id_list).is_instance_of(list).contains_only(id1)


def test_fetch_one_with_id():

    data_dict = m.fetch(
        match = id1,
        collection="testcollection"
    )
    
    # print("\n\\ test_fetch_with_id:: data_dict, id1", data_dict, list(data_dict), id1)

    assert_that(data_dict).contains_entry({"_id": id1})
    assert_that(data_dict['age']).is_instance_of(int)
    assert_that(data_dict['birthdate']).is_instance_of(dt.datetime)



def test_insert_many():
    
    id_list = m.insert(
        schema=DummySchema, 
        collection="testcollection",
        data=[
            dummy_data, 
            dummy_data,
            dict(dummy_data, **{"_id": str(uuid.uuid4())})
        ]
    )
    
    #print("\ntest_insert_many:: id_list", id_list)

    assert_that(id_list).is_not_none().is_length(3)



def test_fetch_all_with_match():

    datagen = m.fetch(
        match = {'name': 'John Show'},
        collection="testcollection",
        
    )
    
    # print("\ntest_fetch_all_with_match:: datagen", datagen, type(datagen))

    assert_that(len(list(datagen))).is_greater_than_or_equal_to(1)



def test_update_list_with_append():

    data_list = [
        {
            "name": "Dan lupin",
            "some_field": "this should remain unchanged"
        },

        {
            "test_list": ["initial_list_value"], 
            "test_list2": [ "initial_list_value2"],
            "test_dict": {"initial_dict_key":"initial_dict_value"},
            "test_list_of_dict": [
                {"initial_dict_key":"initial_dict_value", "some_id":"asdasdasd"},
                {"initial_dict_key":"initial_dict_value", "some_id":"dsadsadsa"}
            ],
            "name": "arsene lupin",
            "some_field": "this should remain unchanged"
        }
    ]

    id_list = m.insert(AnotherDummySchema, "testcollection", data_list)

    assert_that(len(id_list)).is_equal_to(len(data_list))

    new_data = {
        "_id": "thenewid",
        'name': 'Dan', 
        "test_list": ["appended_value"],
        "test_list2": [ "appended_value2"],
        "test_dict": {"new_dict_key":"new_dict_value"},
        "test_list_of_dict": [
            {"new_dict_key":"new_dict_value"}
        ]
    }

    updated_data = m.update(
        schema     = AnotherDummySchema,
        collection ="testcollection",
        match      = {'test_list': { "$exists": True }},
        new_data   = new_data,
        append     = True
    )

    # print(updated_data)

    data = m.fetch(
        match = {'test_list': { "$exists": True }},
        collection="testcollection",
    )

    # print(data)
    
    assert_that(data[0]['test_list']).contains('initial_list_value')
    assert_that(data[0]['test_list2']).contains('initial_list_value2')
    assert_that(data[0]['test_dict']['initial_dict_key']).contains('initial_dict_value')
    assert_that(data[0]['some_field']).contains('this should remain unchanged')




def test_update_new_doc():
    
    new_data = {
        "_id": existing_id,
        "name": "radu"
    }

    updated_data = m.update(
        schema = AnotherDummySchema,
        collection="testcollection",
        match      = new_data["_id"],
        new_data   = new_data,
        append     = True
    )


    data = m.fetch(
        match = new_data["_id"],
        collection="testcollection",
    )

    # print(data)

    assert_that(data).is_equal_to(new_data)
    


def test_update_new_doc_existing_id():
    
    new_data = {
        "_id": existing_id,
        "name": "cornelia"
    }

    updated_data = m.update(
        schema = AnotherDummySchema,
        collection="testcollection",
        match      = new_data["_id"],
        new_data   = new_data,
        append     = True
    )


    data = m.fetch(
        match = new_data["_id"],
        collection="testcollection",
    )

    assert_that(data).is_equal_to(new_data)



def test_existing_id():
    test_update_new_doc()
    test_update_new_doc_existing_id()


def test_update_id_field_match():

    new_data = {
        "_id": existing_id,
        "name": "razvan",
        "test_list": ["data"]
    }

    updated_data = m.update(
        schema = AnotherDummySchema,
        collection="testcollection",
        match      = {"_id": existing_id,"name": "cornelia"},
        new_data   = new_data,
        append     = True
    )

    data = m.fetch(
        match = new_data["_id"],
        collection="testcollection",
    )

    # print(data)

    assert_that(data['_id']).is_equal_to(new_data["_id"])



def test_update_one_with_id():

    response = m.update(
        schema= AnotherDummySchema,
        collection = "testcollection",
        match      = id1,
        new_data   = {'name': 'New John Show'},
        append     = True
    )
    
    #print(response)

    assert_that(response).is_equal_to(1)



def test_update_all_with_match():
    
    import re
    regx = re.compile("^New John", re.IGNORECASE)

    response = m.update(
        schema= AnotherDummySchema,
        collection = "testcollection",
        match      = {'name': regx},
        new_data   = {'name': 'John'},
        append     = True
    )

    #print(response)

    assert_that(response).is_greater_than_or_equal_to(1)



def test_update_with_pullall():

    _id = str(uuid.uuid4())

    data = {
        "_id": _id,
        "name": "licenseware",
        "test_list": [1,2,3],
        "test_dict": {"nbr":2},
        "test_list_of_dict": [
            {"file_id": "should be unique", "other_data": "some data"},
            {"file_id": "thefileid", "other_data": "some data"}
        ]
    }

    inserted = m.insert(AnotherDummySchema, "testcollection", data)

    assert_that(inserted).contains_only(_id)

    new_data = {
        "_id": _id,
        "name": "licenseware_new",
        "test_list_of_dict": [
            {"file_id": "should be unique", "other_data": "changed a little"},
        ]
    }


    m.update(
        AnotherDummySchema,
        match=_id,
        new_data=new_data,
        collection="testcollection",
        append     = True
    )

    saved_data = m.fetch(_id, "testcollection")

    print(saved_data)












def test_fetch_with_agreggate():

    doc_list = m.aggregate(
        collection = "testcollection",
        pipeline   = [{ "$match": {'name': 'John'} }],
        as_list = True        
    )

    # print(doc_list)

    assert_that(doc_list).is_instance_of(list).is_not_empty()


def test_fetch_distinct():

    doc_list = m.fetch(
        match = 'name',
        collection = "testcollection",
        as_list = True        
    )

    # print(doc_list)

    assert_that(doc_list).is_instance_of(list).is_not_empty()



def test_delete_by_id():

    deleted_docs_nbr = m.delete(
        collection = "testcollection",
        match      = id1,
    )

    #print(deleted_docs_nbr)

    assert_that(deleted_docs_nbr).is_equal_to(1)



def test_delete_with_query():

    deleted_docs_nbr = m.delete(
        collection = "testcollection",
        match      = {'name': 'John'},
    )

    #print(deleted_docs_nbr)

    assert_that(deleted_docs_nbr).is_greater_than_or_equal_to(1)



def test_delete_collection():

    deleted_col_nbr = m.delete_collection(collection="testcollection")

    # print(deleted_col_nbr)

    assert_that(deleted_col_nbr).is_equal_to(1)







