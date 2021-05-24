"""

This module makes available the `namespace` decorator 
which can be used to generate flask_restx namespace from marshmallow schema

```py

from licenseware.decorators import namespace, login_required
from marshmallow import fields, Schema


class CatSchema(Schema):
	_id = fields.Integer(required=True)
	name = fields.String(required=True)


# Can be done in 2 ways

# 1. using the namespace decorator

@namespace(schema=CatSchema, collection='MongoCollectionName', decorators=[login_required])
class CatNamespace: 
	# overwrite get, post, put, delete methods
	...


# or  
# 2. Using the SchemaNamespace class with the defaults

DeviceNamespace = SchemaNamespace(
    schema=DeviceSchema, 
    collection='IFMPData', 
    methods=['GET', 'POST']
)


```

The example up provides all basic CRUD operations and swagger documentation.


If you decide to overwrite get, post, put, delete requests you can provide function parameters as query parameters.
You can retrive them with flask's `request.args`.
Query parameters MUST be set to None (ex: `def get(self, param1=None, param2=None): ...`)

Once your CRUD implementation is done you can import `CatNamespace` class in your namespace gatherer file:

```py

from flask import Blueprint
from flask_restx import Api

from .mymodule import CatNamespace

blueprint = Blueprint('api', __name__)
api = Api(blueprint, title='My title', version='1.0')

api.add_namespace(CatNamespace(), path='/schema')

```

`CatNamespace()` will return the flask_restx namespace generated.

"""

import re
import uuid
import logging
import datetime
from inspect import signature
from marshmallow import Schema
from marshmallow_jsonschema import JSONSchema

from flask import request
from flask_restx import (
	abort,
	Namespace, 
	Resource
)

import licenseware.mongodata as m
from licenseware.decorators import authorization_check



auth_header_doc = {
	'TenantId': {
		'type': 'apiKey',
		'in': 'header',
		'name': 'TenantId'
	},
	'Authorization': {
		'type': 'apiKey',
		'in': 'header',
		'name': 'Authorization'
	}
}



class MongoRequests:
	"""
		This class provides get, post, put, delete http methods.

		Needs a TenantId in the request header.	
		Decorator authorization_check makes sure that TenantId and auth_token are provided

		Query params are taken from request.args, '_id' parameter is just for swagger documentation.

	"""

	request_obj = None # This will be updated when a http request is made

	def get(self, _id=None):
		if 'GET' in self.methods: 
			return self.fetch_data(request) 
		return "METHOD NOT ALLOWED", 405

	def post(self):
		if 'POST' in self.methods:
			return self.insert_data(request) 
		return "METHOD NOT ALLOWED", 405
		
	def put(self):
		if 'PUT' in self.methods:
			return self.update_data(request) 
		return "METHOD NOT ALLOWED", 405
		
	def delete(self, _id=None):
		if 'DELETE' in self.methods:
			return self.delete_data(request) 
		return "METHOD NOT ALLOWED", 405


	@property
	def params(self):
		params = {}
		if self.request_obj.args is None: return params
		params = dict(self.request_obj.args) or {}
		params.pop('tenant_id', None)
		return params

	@property
	def payload(self):
		payload = {}
		if self.request_obj.json is None: return payload
		if isinstance(self.request_obj.json, dict):
			payload = self.request_obj.json
			payload.pop('tenant_id', None)

		return payload
		
	@property
	def query(self):
		tenant = {'tenant_id': self.request_obj.headers.get("TenantId")}
		query  = { **tenant, **self.params,  **self.payload }
		logging.warning(f"CRUD Request: {query}")
		return query


	def fetch_data(self, request_obj):
		self.request_obj = request_obj
		
		results = m.fetch(match=self.query, collection=self.collection)

		if isinstance(results, str):
			abort(500, reason=results)

		if not results: 
			abort(404, reason='Requested data not found')

		return results


	def update_data(self, request_obj):
		self.request_obj = request_obj
		
		updated_docs = m.update(
			schema=self.schema, 
			match=self.query,
			new_data=dict(self.query, **{"updated_at": datetime.datetime.utcnow().isoformat()}), 
			collection=self.collection,
			append=False
		)

		if updated_docs == 0:
			abort(404, reason='Query had no match')

		if isinstance(updated_docs, str):
			abort(500, reason=updated_docs)

		return "SUCCESS"


	def insert_data(self, request_obj):
		self.request_obj = request_obj

		data = dict(self.query, **{
			"_id": str(uuid.uuid4()), 
			"updated_at": datetime.datetime.utcnow().isoformat()}
		)
		
		inserted_docs = m.insert(
			schema=self.schema, 
			collection=self.collection,
			data=data
		)

		if len(inserted_docs) == 0:
			abort(404, reason='Could not insert data')

		if isinstance(inserted_docs, str):
			abort(500, reason=inserted_docs)

		return "SUCCESS"


	def delete_data(self, request_obj):
		self.request_obj = request_obj
		
		deleted_docs = m.delete(match=self.query, collection=self.collection)
		
		if deleted_docs == 0:
			abort(404, reason='Query had no match')

		if isinstance(deleted_docs, str):
			abort(500, reason=deleted_docs)

		return "SUCCESS"



class SchemaNamespace(MongoRequests):
	"""
		This class creates the Namespace object from Schema 
		
		DeviceNamespace = SchemaNamespace(
			schema=DeviceSchema, 
			collection='IFMPData', 
			methods=['GET', 'POST']
		)

	"""

	# Used by namespace decorator
	schema = None
	collection = None
	decorators = None
	methods = None # allowed methods(the rest will get a 405)
	authorizations = None # authorization_check is used by default

	def __init__(self, 
	schema: Schema = None, 
	collection: str = None, 
	methods: list = ['GET', 'POST', 'PUT', 'DELETE'], 
	decorators: list = [authorization_check], 
	authorizations: dict = None
	):
		self.schema = self.schema or schema
		self.collection = self.collection or collection
		self.decorators = self.decorators or decorators
		self.methods = self.methods or methods
		self.authorizations = self.authorizations or authorizations or auth_header_doc

		self.schema_name = self.schema.__name__
		self.name = self.schema_name.replace("Schema", "")
		self.path = "/" + self.name.lower()
		self.json_schema = None
		self.ns = None
		self.model = None
		self.resources = None
		self.http_methods = None


	@classmethod
	def _initialize(cls):
		c = cls(cls.schema, cls.decorators, cls.authorizations)
		return c.initialize()

	def __call__(self):
		newcls = type(self.name, (SchemaNamespace,), {**self.__dict__})
		return newcls._initialize()
	
	def initialize(self) -> Namespace:
		""" Create restx api namespace from schema """

		self.ns = self.create_namespace()
		self.make_json_schema()
		self.model = self.ns.schema_model(self.name, self.json_schema)  
		self.attach_http_methods()
		self.attach_http_docs()
		
		self.resources = self.create_resources()
		self.attach_resources()

		return self.ns

	def create_namespace(self) -> Namespace:        
		ns = Namespace(
			name = self.name, 
			description = f"API is generated from {self.schema_name}",
			decorators = self.decorators, 
			authorizations = self.authorizations,
			security = list(self.authorizations.keys())
		)
		return ns


	def create_resources(self) -> list:

		resource_list = []
		for http_verb, dict_ in self.http_methods.items():

			@self.ns.doc(**dict_['docs'])
			class BaseResource(Resource): ...
			
			resource = type(
				self.name + http_verb.capitalize(), 
				(BaseResource,), 
				{http_verb: dict_['method']}
			)

			base_route = self.path + '/' + http_verb.lower()
			routes = [base_route]

			# TODO parameters from function parameters
			# if 'params' in dict_['docs']:
			#     print("-------- params:", dict_['docs']['params'])
			#     for param in dict_['docs']['params']:
			#         routes.append(base_route + '/' + param)

			resource_list.append((resource, *routes))

		return resource_list


	def attach_resources(self):
		for resource in self.resources:
			self.ns.add_resource(*resource)


	def attach_http_methods(self):
		self.http_methods = {
			"get"   : {'method': self.get,    'docs': None},
			"post"  : {'method': self.post,   'docs': None},
			"put"   : {'method': self.put,    'docs': None},
			"delete": {'method': self.delete, 'docs': None}
		} if self.http_methods is None else self.http_methods


	def attach_http_docs(self):

		for k in self.http_methods.keys():
			self.http_methods[k]['docs'] = {
				'id': f'{k.upper()} request for {self.name}',
				'description': f'Make a {k.upper()} request on {self.name} data.',
				'responses':{
					200: 'SUCCESS',
					500: 'INTERNAL ERROR',
					401: 'UNAUTHORIZED',
					405: 'METHOD NOT ALLOWED',
				},
				'model':self.model,
				'security': list(self.authorizations.keys())
			}

			if k in ['post', 'put', 'delete']:
				self.http_methods[k]['docs'].update({'body':self.model})

			sig = signature(self.http_methods[k]['method'])
			raw_params = list(dict(sig.parameters).keys())
			
			if raw_params:
				self.http_methods[k]['docs'].update({"params": {}})
				for param_name in raw_params:
					param_type = re.search(r"<class '(.*?)'>", str(sig.parameters[param_name].annotation)).group(1)
					param_type = 'str' if param_type == 'inspect._empty' else param_type
					self.http_methods[k]['docs']["params"].update(
						{ param_name:  f"Query parameter ({param_type})"}
					)

				
	def make_json_schema(self) -> dict:
		self.json_schema = JSONSchema().dump(self.schema())["definitions"][self.schema_name]





def namespace(**dkwargs):
	""" 
		This is a class decorator which receives SchemaNamespace keyword arguments

		@namespace(schema=DeviceSchema, collection='IFMPData', methods=['GET'])
		class DeviceNamespace: 

			# overwrite 
			# get, fetch_data, put, update_data, post, insert_data, delete, delete_data
			# methods if needed
		
	"""

	def wrapper(cls):
		newcls = type(cls.__name__, (cls, SchemaNamespace,), {**dkwargs})
		return lambda: newcls._initialize()
	return wrapper
