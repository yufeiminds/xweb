# -*- coding: utf-8 -*-

"""
    xweb.errorlog
    ~~~~~~~~~~~~~

    Error logging.
"""

import logging
from flask import jsonify
from webargs.flaskparser import parser

from . import Component
from ..exception import Error

logger = logging.getLogger(__name__)


class ErrorLog(Component):
    def invoke(self, app):
        @app.errorhandler(Error)
        def exception_handler(e):
            logger.exception(e)
            return jsonify(dict(
                exception='Error',
                message=e.message,
                data=e.data,
                code=e.error_code
            )), 500

        @app.errorhandler(Exception)
        def exception_handler(e):
            logger.exception(e)
            return jsonify(dict(
                exception=e.__class__.__name__,
                message=e.message,
                data=None,
                code=0
            )), 500

        @app.errorhandler(401)
        def exception_handler(e):
            logger.exception(e)
            return jsonify(dict(
                exception=e.__class__.__name__,
                message='Unauthenticated',
                data=None,
                code=getattr(e, 'error_code', 401)
            )), 401

        @parser.error_handler
        def webargs_error_handler(e):
            raise Error(Error.ARGUMENT_ERROR, data=e.message)
