from typing import List
from flask import request
from flask_restx import Namespace, Resource
from licenseware.namespace_generator.schema_namespace import auth_header_doc
from licenseware.registry import AppDefinition, Uploader
from licenseware.editable_table import editable_tables_from_schemas
from licenseware.decorators import (
    authorization_check, 
    machine_check,
    failsafe
)



class AppCreator:
    def __init__(
        self, 
        app_kwargs: dict,
        uploaders_kwargs_list: List[dict],
        reports_kwargs_list: List[dict],
        **kwargs
    ):
        self.app_kwargs = app_kwargs
        self.uploaders_kwargs_list = uploaders_kwargs_list
        self.reports_kwargs_list = reports_kwargs_list
        self.kwargs = kwargs
        
        self.ns = None
        self.app_definition = AppDefinition(**app_kwargs)
        self.uploaders = [ Uploader(**kwargs) for kwargs in uploaders_kwargs_list ]
        self.reports = []
        
        
    def initialize(self):
        # Entrypoint
        self.create_namespace()
        
        self.add_app_route()
        self.add_app_activation_route()
        self.add_register_all_route()
        self.add_editable_tables_route()
        
        self.add_uploads_filenames_validation_routes()
        self.add_uploads_filestream_validation_routes()
        self.add_uploads_status_routes()
        self.add_uploads_quota_routes()
        self.add_uploads_history_routes()
        
        self.app_definition.register_all(
            uploaders = self.uploaders,
            reports   = self.reports
        )
        
        return self.ns
        
        
    def create_namespace(self):
        
        self.ns = Namespace(
            name = self.app_kwargs['name'], 
            description = self.app_kwargs['description'],
            authorizations = auth_header_doc,
            security = list(auth_header_doc.keys())
        )
                
                
    def add_register_all_route(self):
        
        class RegisterAll(Resource):
            @machine_check
            @self.ns.doc("Register all reports and uploaders")
            def get(self):

                response_ok = self.app_definition.register_all(
                    reports = self.reports_kwargs_list.get('reports_list', []), 
                    uploaders = self.uploaders_kwargs_list.get('uploaders_list', [])
                )
                
                if response_ok:
                    return {
                            "status": "success",
                            "message": "Reports and uploaders registered successfully"
                        }, 200
                else:
                    return {
                            "status": "fail",
                            "message": "Reports and uploaders registering failed"
                        }, 500
                    
        
        self.ns.add_resource(RegisterAll, '/register_all')
        
                    
    def add_editable_tables_route(self):
        
        class EditableTables(Resource):
            @failsafe(fail_code=500)
            @authorization_check
            def get(self):
                    return editable_tables_from_schemas(
                        self.app_kwargs['editable_tables_schemas_list']
                    )
        
        self.ns.add_resource(EditableTables, '/editable_tables')
                    
                         
    def add_app_route(self):
        
        class AppRegistration(Resource):
            @failsafe(fail_code=500)
            @machine_check
            @self.ns.doc("Send post with app information to /apps")
            def get(self):
                return self.app_definition.register_app() 
            
        self.ns.add_resource(AppRegistration, '/app')
                  
                  
    def add_app_activation_route(self):
        
        class InitializeTenantApp(Resource):
            @failsafe(fail_code=500)
            @authorization_check
            @self.ns.doc("Initialize app for tenant_id")
            def get(self):
                
                tenant_id = request.headers.get("TenantId")

                for uploader in self.uploaders:
                    qmsg, _ = uploader.init_quota(tenant_id)
                    if qmsg['status'] != 'success':
                        return {'status': 'fail', 'message': 'App failed to install'}, 500
                
                dmsg, _ = self.app_definition.register_app()
                
                if dmsg['status'] != 'success':
                    return {'status': 'fail', 'message': 'App failed to register'}, 500
            
                return {'status': 'success', 'message': 'App installed successfully'}, 200

                    
        self.ns.add_resource(InitializeTenantApp, '/app/init')


    def add_uploads_filenames_validation_routes(self):
                    
        for uploader in self.uploaders:
                
            class FilenameValidate(Resource): 
                @failsafe(fail_code=500)
                @authorization_check
                @self.ns.doc('Validate file name')
                def post(self):
                    return uploader.validate_filenames(request)

            self.ns.add_resource(FilenameValidate, "/uploads" + uploader.upload_validation_url)

    
    def add_uploads_filestream_validation_routes(self):
                    
        for uploader in self.uploaders:
            
            class FileStreamValidate(Resource): 
                @failsafe(fail_code=500)
                @authorization_check
                @self.ns.doc('Validate file contents')
                @self.ns.doc(params={'clear_data': 'Boolean parameter, warning, will clear existing data'})
                def post(self):
                    
                    clear_data = request.args.get('clear_data', 'false')
                    if 'true' in clear_data.lower():
                        self.kwargs['clear_tenant_data_func'](request.headers.get("TenantId"))

                    return uploader.upload_files(request)

            self.ns.add_resource(FileStreamValidate, "/uploads" + uploader.upload_url)

        
    def add_uploads_quota_routes(self):
                    
        for uploader in self.uploaders:
                                
            class UploaderQuota(Resource): 
                @failsafe(fail_code=500)
                @authorization_check
                @self.ns.doc('Check if tenant has quota within limits') 
                def get(self):
                    return uploader.check_quota(request.headers.get("TenantId"))
                
            self.ns.add_resource(UploaderQuota, "/uploads" + uploader.quota_validation_url)
            

    def add_uploads_status_routes(self):
          
        for uploader in self.uploaders:
                  
            class UploaderStatus(Resource): 
                @failsafe(fail_code=500)
                @authorization_check
                @self.ns.doc('Get processing status of files uploaded') 
                def get(self):
                    return self.kwargs['processing_status_func'](request.headers.get("TenantId")) 
                
            self.ns.add_resource(UploaderStatus, "/uploads" + uploader.status_check_url)
            
            
    def add_uploads_history_routes(self):
          
        for uploader in self.uploaders:
                  
            class UploaderHistory(Resource): 
                @failsafe(fail_code=500)
                @authorization_check
                @self.ns.doc('Get the list of actions the tenant made in the past') 
                def get(self):
                    return {"detail": "not implemented"}, 500 

            self.ns.add_resource(UploaderHistory, "/uploads" + uploader.history_url)

    