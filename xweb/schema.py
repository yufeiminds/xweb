# -*- coding: utf-8 -*-

"""
xweb.schema
~~~~~~~~~~~

Api schema base on:

Json-Schema: http://json-schema.org/
OpenAPI: https://openapis.org/

If the schema has been compiled, it wiil be set as read-only.
"""

import copy
from six import iteritems
import marshmallow as ma
from .utils import load_ref


class OpenAPIDataTypes(object):
    def __init__(self, type, format=None, location=None, required=False, description=None,
                 items=None, default=None, *args, **kwargs):
        self.type = type
        self.format = format
        self.location = location
        self.required = required
        self.description = description
        self.items = items
        self.default = default

        assert items if type == 'array' else True, \
            'Item must be existed when data type is array'


class MarshMallowDataTypes(OpenAPIDataTypes):
    DT_MAPS_MA = {
        'string': {
            'byte': ma.fields.Str,
            'binary': ma.fields.Raw,
            'date': ma.fields.Date,
            'date-time': ma.fields.DateTime,
            'password': ma.fields.Str,
            'email': ma.fields.Email,
            'url': ma.fields.URL,
            None: ma.fields.Str
        },
        'integer': {
            'int32': ma.fields.Int,
            'int64': ma.fields.Int,
            None: ma.fields.Int
        },
        'number': {
            'float': ma.fields.Float,
            'double': ma.fields.Float,
            None: ma.fields.Float
        },
        'boolean': {
            None: ma.fields.Bool
        }
    }

    def __call__(self, *args, **kwargs):
        DataType = self.DT_MAPS_MA.get(self.type, {}).get(self.format)
        assert DataType, 'Invalid data type.'
        kwargs = {
            'required': self.required,
            'default': self.default,
            'metadata': {
                'description': self.description
            }
        }
        if self.location:
            if self.location == 'path':
                kwargs['location'] = 'view_args'
            else:
                kwargs['location'] = self.location
        return DataType(**kwargs)


class Schema(object):
    swagger = '2.0'
    info = {
        'title': None,
        'description': None,
        'version': '0.1.0'
    }
    host = None
    schemes = ['http']
    basePath = '/v' + info.get('version')[0]
    produces = ['application/json']
    paths = {}


class SwaggerReader(object):
    def __init__(self, ref):
        self.swagger = {}
        self.load(ref)

    def resolve_ref(self, ref):
        _top = self.swagger or {}
        if '#/' not in ref:
            resource, anchor = ref, ''
        else:
            resource, anchor = ref.split('#/')
        if resource:
            _top = load_ref(resource)

        fields = anchor.split('/')
        for field in filter(lambda x: x, fields):
            _top = _top.get(field)
        return _top

    def load(self, ref):
        self.swagger = self.resolve_ref(ref)
        self.traversal(self.swagger)
        return self.swagger

    def traversal(self, obj):
        """
        .. note:: It will change this object (Not immutable).
        """
        if isinstance(obj, list):
            [self.traversal(item) for item in obj]
        elif isinstance(obj, dict):
            if '$ref' in obj:
                ref = obj.pop('$ref')
                obj.update(self.resolve_ref(ref) or {})
            else:
                [self.traversal(v) for k, v in iteritems(obj)
                 if isinstance(v, list) or isinstance(v, dict)]


class MarshMallowProcessor(object):
    def __call__(self, schema):
        schema = copy.copy(schema)
        _schema = Schema()
        _paths = schema.get('paths', [])
        for k, v in iteritems(schema):
            setattr(_schema, k, v)
        for path, _item in iteritems(_paths):
            for method, api in iteritems(_item):
                parameters = api.get('parameters')
                if not parameters:
                    continue

                class MarshMallowSchema(ma.Schema):
                    class Meta:
                        strict = True

                MarshMallowSchema.__name__ = method.title() + path[1:].title()
                MarshMallowSchema.__doc__ = api.get('description')
                for parameter in parameters:
                    parameter['location'] = parameter.pop('in', None)
                    MarshMallowSchema._declared_fields.update({
                        parameter['name']: MarshMallowDataTypes(**parameter)()
                    })
                _schema.paths[path][method]['parameters'] = MarshMallowSchema
        return _schema


class ThriftProcessor(object):
    def __call__(self, schema):
        pass


openapi_to_marshmallow = MarshMallowProcessor()
openapi_to_thrift = ThriftProcessor()
