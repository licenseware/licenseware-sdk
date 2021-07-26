"""

# history_controller.py

from app.main.report_creator import ReportCreator
from app.main.reports.history_report import components, filters


HistoryReport = ReportCreator(
    app_id='ifmp-service',
    report_id="ifmp_history_report_v1",
    report_name="IFMP History Report",
    description="Provides a detailed overview of the procesed files/devices.",
    url='/history_report',
    connected_apps=['ifmp-service'],
    components=components,
    filters=filters
)

# Get the api
api = HistoryReport.api 

# Get the report
report = HistoryReport.report



# Where do components and filters come from?

They come from : `app.main.reports.history_report` (preferably package with components and filters)

reports
├── history_report
│   ├── components_filter_register.py
│   ├── components_register.py
│   ├── __init__.py

In `__init__.py` import components and filters so you can use this import line later:

```py
from app.main.reports.history_report import components, filters
```
Where `history_report` is a package with your report (device_report, another_report etc)

# Example component from `components_register.py`:

history_overview_data = {
    "component_id": "history_overview",
    "url": "/overview",
    "order": 1,
    "style_attributes": {
        "width": "1/3"
    },
    "attributes": {
        "series": [
            {
                "value_description": "Devices Analyzed",
                "value_key": "devices_analyzed"
            },
            {
                "value_description": "Files Analyzed",
                "value_key": "files_analyzed"
            }
        ]
    },
    "title": "Overview",
    "type": "summary",
    "icon": "name_of_icon.png",
}



# Example data_method from `service`:

class HistoryService:
    
    @staticmethod
    def history_overview(_request, _filter=None):
        
        pipeline = [
            {
                '$match': {
                    'tenant_id': _request.headers.get('TenantId'),
                }
            }, {
                '$unwind': {
                    'path': '$devices', 
                    'preserveNullAndEmptyArrays': False
                }
            }, {
                '$group': {
                    '_id': None, 
                    'devices_analyzed': {
                        '$addToSet': '$device_name'
                    }, 
                    'files_analyzed': {
                        '$addToSet': '$file_name'
                    }
                }
            }, {
                '$project': {
                    '_id': 0, 
                    'devices_analyzed': {
                        '$size': '$devices_analyzed'
                    }, 
                    'files_analyzed': {
                        '$size': '$files_analyzed'
                    }
                }
            }
        ]
                
        if _filter:
            pipeline.insert(0, _filter)
            
        
        return mongodata.aggregate(
            pipeline=pipeline,
            collection=collection_name
        )


# Components list contains tuples with metadata and methods that will fetch the data

components = [
    ( history_overview_data, HistoryService.history_overview ),
    ( data, data_method ),
    etc
]


# Example how filters looks (`components_filter_register.py`):

filters = [
    {
        "column": "device_name",
        "allowed_filters": [
            "equals", "contains", "in_list"
        ],
        "visible_name": "Device Name"
    },
    {
        "column": "updated_at",
        "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
        ],
        "visible_name": "Last Update Date"
    }
]



"""


from flask import request
from flask_restx import Namespace, Resource, fields

from licenseware.namespace_generator.schema_namespace import auth_header_doc
from licenseware.registry.standard_report import (
    StandardReport,
    StandardReportComponent,
    ReportFilteringComponent
)
from licenseware.decorators import (
    failsafe, 
    authorization_check
)

from typing import List, Tuple, Callable
from licenseware.utils.log_config import log



class ReportCreator:
    
    def __init__(
        self, 
        app_id: str, 
        report_id: str,
        report_name: str,
        description: str,
        url: str,
        connected_apps: list,
        components: List[Tuple[List, Callable]],
        filters: list
    ):
        self.app_id = app_id
        self.report_id = report_id
        self.report_name = report_name
        self.description = description
        self.url = url
        self.connected_apps = connected_apps
        
        self.components = components
        self.filters = filters
        
        self.ns = None
        self.filter_model = None
        self.standard_report = None
        # self.resource_list = []
        
        # Create report on init
        self.create_standard_report()
        self.register_components()
        self.register_filters()
        self.standard_report.register_report()
        
        
    @property
    def api(self):
        """Get the restx namespace api"""
        
        self.create_namespace()
        self.create_filter_model()
        self.add_report_register_route()
        self.add_report_route()
        self.add_components_routes()
        # self.add_resources()
        
        return self.ns
    
    
    @property
    def report(self):
        """ Get the instantiated report """
    
        return self.standard_report
        
        
    def create_namespace(self):
        
        self.ns = Namespace(
            name = self.report_name, 
            description = self.description,
            authorizations = auth_header_doc,
            security = list(auth_header_doc.keys()), 
            decorators = [authorization_check]
        )
        
        
    def create_filter_model(self):
        
        self.filter_model = self.ns.model(self.report_name, {
            'column': fields.String(required=True),
            'filter_type': fields.String(required=True),
            'filter_value': fields.List(fields.String, required=False)
        })

                        
    def create_standard_report(self):
        
        self.standard_report = StandardReport(
            app_id=self.app_id,
            report_id=self.report_id,
            report_name=self.report_name,
            description=self.description,
            url=self.url,
            connected_apps=self.connected_apps
        )
        
        
    def register_components(self):
        
        for data, method in self.components:
            self.standard_report.register_component(
                StandardReportComponent(data=data, data_method=method)
            )
            
                    
    def register_filters(self):
        
        self.standard_report.register_filter(
            ReportFilteringComponent(
                filter_columns=self.filters
            )
        )
        
        
    def add_report_register_route(self):
        
        Report = self.standard_report
        
        class ReportRegister(Resource):         
            @failsafe(fail_code=500)   
            @self.ns.doc(f"Register {self.report_name} report")
            def post(self):
                return Report.register_report()
            
        self.ns.add_resource(ReportRegister, self.url + '/register')


    def add_report_route(self):
            
        Report = self.standard_report
        
        class ReportController(Resource):
            @failsafe(fail_code=500)
            @self.ns.doc("Get components metadata") 
            def get(self):
                return Report.return_json_payload()
            
        self.ns.add_resource(ReportController, Report.url)



    def create_component_resource(self, Report, data):
        
        class Data:
                component_id = data['component_id']
                
        class BaseResource(Resource):
            
            @failsafe(fail_code=500)
            @self.ns.doc(f"Get data for {Data.component_id}")
            def get(self):
                
                return Report.components[Data.component_id].return_component_data(_request=request)
            
            @failsafe(fail_code=500)
            @self.ns.doc(f"Filter data for {Data.component_id}")
            @self.ns.marshal_list_with(self.filter_model)
            def post(self):
                filter_payload = request.json
                parsed_filters = Report._filter.build_match_expression(filter_payload)
                return Report.components[Data.component_id].return_component_data(_request=request, _filter=parsed_filters)
        
        
        ComponentResource = type(
            "Report_" + Data.component_id, 
            (BaseResource, Data), 
            {}
        )
        
        
        return ComponentResource, Report.return_component_url(Data.component_id)
        
        
    def add_components_routes(self):
        
        Report = self.standard_report
        
        for data, _ in self.components:
            
            ComponentResource, url = self.create_component_resource(Report, data)
            
            self.ns.add_resource( ComponentResource, url ) 
            
            
            
