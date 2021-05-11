import flask_restx as f
import marshmallow as ma


class EditableTableFactory:

    def __init__(self, _schema: ma.Schema, api: f.Namespace = None):
        self.schema = _schema
        self.api = api if api else f.Namespace(f'Generated model for schema {self.schema.__name__}')
        self.restx_model = self.api.model(
            name=self.schema.__name__,
            model=self.convert_fields_to_restx(self.schema)
        )

    def lware_ui_columns(self):
        pass

    def convert_fields_to_restx(self, _schema: ma.Schema) -> f.model:
        model = {}
        for _field in _schema._declared_fields:
            model[_field] = self.map_field(i_field=_schema._declared_fields[_field])
            print(model)
        return model

    def convert_nested(self, nested_field: ma.fields.Nested):
        out = {}
        for n_field in nested_field.schema._declared_fields:
            out[n_field] = self.map_field(i_field=nested_field.schema._declared_fields[n_field])
        self.api.model(nested_field.name, model=out)
        return out

    def map_field(self, i_field: ma.fields):
        _type = type(i_field)

        if _type is ma.fields.List:
            return f.fields.List(self.map_field(i_field=i_field.inner))
        if _type is ma.fields.Nested:
            return f.fields.Nested(self.api.model(name=i_field.name, model=self.convert_nested(i_field)))

        _map = {
            ma.fields.String: f.fields.String,
            ma.fields.Str: f.fields.String,
            ma.fields.Boolean: f.fields.Boolean,
            ma.fields.Float: f.fields.Float,
            ma.fields.Integer: f.fields.Integer,
            ma.fields.DateTime: f.fields.DateTime,
            ma.fields.Dict: f.fields.Raw,
            ma.fields.Raw: f.fields.Raw

        }
        try:
            return _map[_type](required=i_field.required, description=i_field.metadata.get('description', None),
                                 readonly=i_field.metadata.get('editable', None))
        except (KeyError, AttributeError):
            raise NotImplementedError
