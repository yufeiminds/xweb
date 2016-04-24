# -*- coding: utf-8 -*-

"""
Copyright 2016 Yufei Li <yufeiminds@gmail.com>
"""

import os
from xweb import schema, invoke
import marshmallow as ma

test_dir = os.path.abspath('tests')
swagger_reader = schema.SwaggerReader(os.path.join(test_dir, './files/swagger.yaml'))


def test_swagger_dict_init():
    swagger_dict = swagger_reader.swagger
    assert swagger_dict['swagger'] == '2.0'
    resp_200 =  swagger_dict['paths']['/products']['get']['responses'][200]
    assert resp_200['schema']['items']['type'] == 'object'


def test_swagger_to_marshmallow_schema():
    ma_schema = schema.openapi_to_marshmallow(swagger_reader.swagger)
    assert ma_schema.swagger == '2.0'
    ProductsSchema = ma_schema.paths['/products']['get']['parameters']
    assert issubclass(ProductsSchema, ma.Schema)
    assert isinstance(ProductsSchema.latitude, ma.fields.Float)
    assert ProductsSchema.Meta.strict


def test_invoke_app():
    app = invoke.create_app()
    app.invoke_app()