import datetime
from .log_config import log
import licenseware.mongodata as m
from licenseware.serializer.analysis_status import AnalysisStatusSchema
from marshmallow import Schema
from .base_collection_names import mongo_analysis_collection_name




class FileTimeout:
    
    def __init__(
        self, 
        tenant_id: str = None, 
        schema: Schema = None,
        analysis_collection_name: str = None, 
        low_memory: bool = False
    ) -> None:
        
        self.tenant_id = tenant_id
        self.schema = schema or AnalysisStatusSchema
        self.analysis_collection_name = analysis_collection_name or mongo_analysis_collection_name
        self.low_memory = low_memory


    def get_timed_out_files(self):
            
        time_out_time = datetime.datetime.utcnow() - datetime.timedelta(minutes=30)
        start_time    = datetime.datetime.utcnow() - datetime.timedelta(days=360)
        
        query = {
            '$or': [
                {
                    'files.status': 'Running'
                },
                {
                    'status': 'Running'
                }
            ],
            'updated_at': {
                '$gt': start_time.isoformat(), 
                '$lt': time_out_time.isoformat()
            }
        }
        
        if self.tenant_id: 
            query['tenant_id'] = self.tenant_id

        return m.fetch(
            match = query, 
            collection = self.analysis_collection_name, 
            as_list = not(self.low_memory)
        )


    def close_timed_out(self, timed_out_file: dict):

        timed_out_file["status"] = "Error"
        for file in timed_out_file.get('files', []):
            file['status'] = 'Error'

        return m.update(
            schema=self.schema,
            match=timed_out_file,
            new_data=timed_out_file,
            collection=self.analysis_collection_name
        )
        
        
    def close_timed_out_files(self): 
        """
            Check `AnalysisStats` collection for files that have status: 'Running'
            Set status to `Error` if they are running for more time than specified in `_get_timed_out_files`
            
            low_memory = False : will use a generator to save memory
            
        """
        
        timed_out_files = self.get_timed_out_files()
        
        if isinstance(timed_out_files, str):
            log.error(timed_out_files)
            return
        
        for f in timed_out_files:
            self.close_timed_out(f)
            
            