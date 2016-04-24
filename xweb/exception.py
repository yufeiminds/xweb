# -*- coding: utf-8 -*-

"""
    xweb.exception
    ~~~~~~~~~~~~~~

    Define exceptions.
"""


class Error(Exception):
    """
    User error
    """
    " 0 ~ 1000 System Error "
    BOOTSTRAP_ERROR = 0
    ARGUMENT_ERROR = 1
    DATABASE_ERROR = 2

    " 1000 ~ fin User Error "
    translate = {
        BOOTSTRAP_ERROR: u'System Internal Error',
        ARGUMENT_ERROR: u'Argument Error',
        DATABASE_ERROR: u'Database Error'
    }

    def __init__(self, code, message=None, data=None, **kwargs):
        self.error_code = code
        self.data = data
        self.template = message or self.translate.get(self.error_code)
        self.message = self.template.format(**kwargs)

    def __str__(self):
        return self.message


class XwebException(Exception):
    " Base exception "
    pass


class NoConfigError(XwebException):
    " No config loaded "
    pass


class RemoteServerError(XwebException):
    " For remote server broken error. "
    pass
