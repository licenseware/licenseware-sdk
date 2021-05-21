"""

This module makes available the `namespace` decorator 
which can be used to generate flask_restx namespace from marshmallow schema

```py

from licenseware.decorators import namespace, login_required
from marshmallow import fields, Schema
from flask import request


class CatSchema(Schema):
    _id = fields.Integer(required=True)
    name = fields.String(required=True)


# @namespace(CatSchema, [login_required]) # args works also
@namespace(schema=CatSchema, decorators=[login_required])
class CatNamespace:

    # implement get, post, put, delete methods

    def get(self, param1=None, param2=None): 

        param1 = request.args.get('param1)
        param2 = request.args.get('param1)

        return "your GET request implementation"
    
    def post(self): 
        return "your POST request implementation"

```

As you see in the `get` method param1 and param2 are query parameters.
You can retrive them with flask's `request.args`.
Query parameters MUST be set to None (as you see in get method `def get(self, param1=None, param2=None): ...`)



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
OpenAPI/Swagger docs will be automatically be generated from schema model.

 
"""

import re
import logging
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

    # Used by ns decorator
    schema = None
    decorators = None
    authorizations = None

    def __init__(self, schema: Schema = None, decorators: list = None, authorizations: dict = None):
        self.schema = self.schema or schema
        self.decorators = self.decorators or decorators
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
    def initialize(cls):
        c = cls(cls.schema, cls.decorators, cls.authorizations)
        return c.init_namespace()


    def init_namespace(self) -> Namespace:
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


    def get(self)   : return "Method Not Allowed", 405
    def post(self)  : return "Method Not Allowed", 405
    def put(self)   : return "Method Not Allowed", 405
    def delete(self): return "Method Not Allowed", 405
        



# SchemaApiFactory Decorator 

def get_schema_param(dargs, dkwargs):

    if 'schema' in dkwargs:
        return dkwargs['schema']

    if len(dargs) > 0:
        return dargs[0]

def get_decorators_param(dargs, dkwargs):

    if 'decorators' in dkwargs:
        return dkwargs['decorators']

    if len(dargs) > 1:
        return dargs[1]

def get_authorizations_param(dargs, dkwargs):

    if 'authorizations' in dkwargs:
        return dkwargs['authorizations']

    if len(dargs) > 2:
        return dargs[2]


def get_schema_api_factory_params(dargs, dkwargs):
    return {
        'schema': get_schema_param(dargs, dkwargs), 
        'decorators': get_decorators_param(dargs, dkwargs),
        'authorizations': get_authorizations_param(dargs, dkwargs)
    }




# Namespace generator 
def namespace(*dargs, **dkwargs):
    def wrapper(cls):
        attrs = get_schema_api_factory_params(dargs, dkwargs)
        newcls = type(cls.__name__, (cls, SchemaApiFactory,), attrs)
        return lambda: newcls.initialize()
    return wrapper



