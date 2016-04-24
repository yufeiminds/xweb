# -*- coding: utf-8 -*-

"""
    xweb.components.restful
    ~~~~~~~~~~~~~~~~~~~~~~~

    Restful if yes.
"""

import re
import logging
from six import iteritems
from jsonpickle import dumps
from werkzeug.wrappers import Response
from werkzeug.utils import import_string
from flask import jsonify, Blueprint, request
from webargs.flaskparser import use_args

from . import Component
from ..schema import (
    SwaggerReader,
    openapi_to_marshmallow
)
from ..utils import decorator

logger = logging.getLogger(__name__)
logging.basicConfig()


@decorator
def json_serialize(func, *args, **kwargs):
    LITERAL_TYPES = (str, unicode, int, float, list, type(None))
    result = func(*args, **kwargs)

    if isinstance(result, dict):
        pass
    elif isinstance(result, Response):
        return result
    elif type(result) in LITERAL_TYPES:
        result = {'data': result}
    else:
        result = dumps(result, unpicklable=False)

    return jsonify(result)


@decorator
def cross_domain(func, *args, **kwargs):
    resp = func(*args, **kwargs)
    h = resp.headers

    h['Access-Control-Allow-Origin'] = "*"
    h['Access-Control-Allow-Methods'] = ', '.join(map(str.upper, func.methods))
    h['Access-Control-Max-Age'] = 21600

    return resp


def import_view_function(endpoint):
    logger.debug('import %s', endpoint)
    function = import_string(endpoint)
    return function


def endpoint_from_url(url):
    return re.sub(r'[/\{\}]', '', url.title())


class RestFul(Component):
    def configure(self):
        schema_ref = self.config.get('schema_ref')
        schema_reader = SwaggerReader(schema_ref)
        self.schema = openapi_to_marshmallow(schema_reader.swagger)
        self.decorators = [import_string(_) for _ in self.config.get('decorators', [])]
        self.blueprint = Blueprint(endpoint_from_url(self.schema.basePath), __name__,
                                   url_prefix=self.schema.basePath)

    def create_resource(self, path, resource_schema):
        _map = {}
        path = path.replace('{', '<').replace('}', '>')
        methods = resource_schema.keys()

        for method, api in iteritems(resource_schema):
            view_string = api.get('operationId') or 'xweb.mock.view_func'
            function = import_view_function(view_string)
            function.methods = methods
            function = cross_domain(json_serialize(function))
            if 'parameters' in api:
                function = use_args(api['parameters'])(function)
            for deco in self.decorators:
                function = deco(function)
            _map[method] = function

        def dispatcher(*args, **kwargs):
            meth = request.method.lower()
            fn = _map.get(meth, None)
            if meth is None and meth == 'HEAD':
                fn = _map.get('get', None)
            assert meth is not None, 'Unimplemented method %r' % request.method
            return fn(*args, **kwargs)

        endpoint = endpoint_from_url(path)
        dispatcher.__name__ = endpoint
        dispatcher.__doc__ = 'Dispatcher for {url}'.format(url=path)
        dispatcher.methods = _map.keys()
        self.blueprint.add_url_rule(path, endpoint, dispatcher,
                                    methods=dispatcher.methods)

    def invoke(self, app):
        self.config = app.config.get('restful', dict())
        self.configure()

        for path, schema in iteritems(self.schema.paths):
            self.create_resource(path, schema)

        app.register_blueprint(self.blueprint)
