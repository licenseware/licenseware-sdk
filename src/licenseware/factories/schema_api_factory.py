"""

from licenseware import SchemaApiFactory
from .utils import authorization_check, machine_check

from flask import request
from marshmallow import fields, Schema


class CatSchema(Schema):
    _id = fields.Integer(required=True)
    name = fields.String(required=True)


factory_api = SchemaApiFactory(
    schema = CatSchema, decorators = [authorization_check, machine_check]
)


# Add CRUD implementations


def get_data(resource, catName=None, catId: int = None):
    # Parameter resource is passed by default to all funcs by werkzeug
    
    print("catId, catName: ", catId, catName) #will be None
    print("request.args", request.args)

    # Function parameters will be considered as request args.

    You can retrieve args with: 
    - request.args.get('catName')
    - request.args.get('catId')

    #Your implementation
   

def insert_data(resource): 

    You can retrieve body with:
    - request.json

    #Your implementation
   

def update_data(resource):
    #Your implementation
    

def delete_data(resource):
    #Your implementation


# Overwrite default CRUD methods

factory_api.get = get_data
factory_api.post = insert_data
factory_api.put = update_data
factory_api.delete = delete_data


api = factory_api.initialize()


# In another file
# Import this api to main Api namespace

from .ns_schema import api as schema_api

api.add_namespace(schema_api, path='/schema')



# Or with inheritance

class Cat(SchemaApiFactory):
    def __init__(self, schema: Schema, decorators: list = None):
        super().__init__(schema, decorators)

    # Overwrite CRUD methods: get, put, post, delete


factory_api = Cat(schema=CatSchema, decorators=[authorization_check, machine_check])

api = factory_api.initialize()

# In another file
# Import this api to main Api namespace

from .ns_schema import api as schema_api

api.add_namespace(schema_api, path='/schema')


"""

import re
from marshmallow import Schema
from marshmallow_jsonschema import JSONSchema
from flask_restx import Namespace, Resource
from inspect import signature


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


class SchemaApiFactory:

    def __init__(self, schema: Schema, decorators: list = None, authorizations: dict = None):
        self.schema = schema
        self.schema_name = self.schema.__name__
        self.name = self.schema_name.replace("Schema", "")
        self.decorators = decorators
        self.path = "/" + self.name.lower()
        self.authorizations = authorizations or auth_header_doc
        self.json_schema = None
        self.ns = None
        self.model = None
        self.resources = None
        self.http_methods = None


    def initialize(self) -> Namespace:
        """ Create restx api namespace from schema """

        self.ns = self.create_namespace()
        self.make_json_schema()
        self.model = self.ns.schema_model(self.schema_name, self.json_schema)  
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
                'description': f'Make a {k.upper()} request on {self.name} data.',
                'responses':{
                    200: 'Success',
                    500: 'Internal Error',
                    401: 'Authentification Required',
                    405: 'Method Not Allowed'
                },
                'model':self.model,
                'security': list(self.authorizations.keys())
            }

            if k in ['post', 'put', 'delete']:
                self.http_methods[k]['docs'].update({'body':self.model})

            sig = signature(self.http_methods[k]['method'])
            raw_params = list(dict(sig.parameters).keys())
            if len(raw_params) > 1:
                self.http_methods[k]['docs'].update({"params": {}})
                for param_name in raw_params[1:]:
                    param_type = re.search(r"<class '(.*?)'>", str(sig.parameters[param_name].annotation)).group(1)
                    param_type = 'str' if param_type == 'inspect._empty' else param_type
                    self.http_methods[k]['docs']["params"].update(
                        { param_name:  param_type}
                    )

    
    def make_json_schema(self) -> dict:
        self.json_schema = JSONSchema().dump(self.schema())["definitions"][self.schema_name]


    def get(self): return "Method Not Allowed", 405
    def post(self): return "Method Not Allowed", 405
    def put(self): return "Method Not Allowed", 405
    def delete(self): return "Method Not Allowed", 405
        

