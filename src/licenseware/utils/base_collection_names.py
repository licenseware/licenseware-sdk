"""
This module makes available base collection names used for each service

Ex:
If APP_ID is 'ifmp-service'
Generated collection names will be:
- "IFMPData"
- "IFMPUtilization"
- "IFMPAnalysisStats"

Services names should be named like "XXX-name" where XXX it's a unique acronym.

"""

from .urls import APP_ID


app_prefix = str(APP_ID).split('-')[0].upper() 

mongo_data_collection_name = app_prefix + "Data"
mongo_utilization_collection_name = app_prefix + "Utilization"
mongo_analysis_collection_name = app_prefix + "AnalysisStats"

