from marshmallow import Schema, fields


class AnalysisStatusSchema(Schema):
    tenant_id = fields.Str(required=True)
    status = fields.Str(required=True)
    file_type = fields.Str(required=False)
    
    
