"""

Wrapper for mongodb with tuple response (dict, status code)

from licenseware import DataManagement

dm = DataManagement(collection="Data", schema=SchemaMarshmallowClass)

"""


from marshmallow import ValidationError
from pymongo import errors
from .utils import get_mongo_connection

mongo_db = get_mongo_connection()


class DataManagement:
    def __init__(self, collection, schema):
        self.connection = mongo_db
        self.database = self.connection["db"]
        self.document_schema = schema()
        self.collection = collection

    def collection_db(self):
        collection = self.database[self.collection]
        return collection

    def get_by_id(self, _id):
        try:
            collection = self.database[self.collection]
            result = collection.find_one({"_id": _id})
            result_data = self.document_schema.dump(result)
            if not result_data:
                return {"status": "fail", "message": "id is not found"}, 404
            return result_data, 200
        except errors.ConnectionFailure as e:
            return {"status": "fail", "message": "errors in connection"}, 500

    def get_one_with_filter(self, _filter):
        try:
            collection = self.database[self.collection]
            result = collection.find_one(_filter)
            if not result:
                return {"status": "fail", "message": "id is not found"}, 404
            result_data = self.document_schema.dump(result)
            return result_data, 200
        except errors.ConnectionFailure as e:
            return {"status": "fail", "message": "errors in connection"}, 500

    def get_all(self, _filter=None):
        try:
            # print(f"Get all with filter {_filter}")
            collection = self.database[self.collection]
            results = collection.find(_filter)
            results_data = []
            for result in results:
                results_data.append(self.document_schema.dump(result))
            if len(results_data) < 1:
                return {"status": "fail", "message": "id is not found"}, 404
            return results_data, 200
        except errors.ConnectionFailure as e:
            return {"status": "fail", "message": "errors in connection"}, 500

    def insert_data(self, json_data):
        if not json_data:
            return {"status": "fail", "message": "No input data provided"}, 400
        try:
            data = self.document_schema.load(json_data)
            collection = self.database[self.collection]
            collection.insert_one(data)
        except ValidationError as err:
            print(err)
            return err.messages, 422
        return {"status": "success", "message": "Created new document.", "document": data}, 202

    def replace_one(self, json_data, _filter=None):
        try:
            if _filter is None:
                _filter = {"_id": json_data["_id"]}
            collection = self.database[self.collection]
            result = collection.replace_one(_filter, self.document_schema.load(json_data),
                                            upsert=True)
            new = collection.find_one(_filter)
            return self.document_schema.dump(new), 200
        except errors.ConnectionFailure as e:
            return {"status": "fail", "message": "errors in connection"}, 500

    def update_one(self, json_data, _filter=None):
        try:
            if _filter is None:
                _filter = {"_id": json_data["_id"]}
            collection = self.database[self.collection]
            old = collection.find_one(_filter)
            if old:
                for k in json_data:
                    if "_id" != k:
                        if all(isinstance(elem, list) for elem in [json_data[k], old.get(k, None)]):
                            # logging.warning(k)
                            # both elements are lists, check if they are list of dicts or list of strings because dicts and lists are unhashable
                            if any(isinstance(kv, dict) for kv in old[k]) or any(isinstance(kv, list) for kv in old[k]):
                                # logging.warning(json_data)
                                old[k].extend(json_data[k])
                            else:
                                new_list = list(set().union(old[k], json_data[k]))
                                old[k] = new_list
                        else:
                            # only one element is a list, we replace the old one with the new since the data as been validated by the serializer
                            old[k] = json_data[k]
                return self.replace_one(json_data=self.document_schema.dump(old))
        
            return self.insert_data(json_data) 
        
        except errors.ConnectionFailure as e:
            return {"status": "fail", "message": "errors in connection"}, 500

    def delete_all(self):
        try:
            collection = self.database[self.collection]
            result = collection.delete_many({})
            return {"status": "success", "message": "all data deleted"}, 200
        except errors.ConnectionFailure as e:
            return {"status": "fail", "message": "errors in connection"}, 500

    def delete_one(self, _id):
        try:
            collection = self.database[self.collection]
            result = collection.delete_one({"_id": _id})
            return {"status": "success", "message": "data deleted"}, 200
        except errors.ConnectionFailure as e:
            return {"status": "fail", "message": "errors in connection"}, 500

    def get_with_aggregation(self, pipeline):
        try:
            collection = self.database[self.collection]
            results = collection.aggregate(pipeline)
            results_data = []
            for r in results:
                results_data.append(self.document_schema.dump(r))
            return results_data, 200
        except errors.ConnectionFailure as e:
            return {"status": "fail", "message": "errors in connection"}, 500
