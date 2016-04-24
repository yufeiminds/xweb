# -*- coding: utf-8 -*-

"""
xweb.components
~~~~~~~~~~~~~~~

Flask components(extensions).
"""


class Component(object):
    " Abstract class for component "

    def __init__(self, app=None):
        self.app = app

    def invoke(self, app):
        raise NotImplementedError

    def init_app(self):
        self.invoke(self.app)