# -*- coding: utf-8 -*-

"""

    xweb.invoke
    ~~~~~~~~~~~

    Invoke flask app.

"""

import os.path
from flask import Flask
from pprint import pprint
from operator import attrgetter

from .utils import load_ref
from .exception import NoConfigError
from .components.restful import RestFul
from .components.errorlog import ErrorLog


class Base(Flask):
    " Abstract class for app "

    _components = []

    def load_config(self, ref=None):
        raise NotImplementedError

    def invoke_app(self):
        raise NotImplementedError

    def use(self, component):
        self._components.append(component)

    @property
    def components(self):
        return self._components


class App(Base):
    def load_config(self, ref=None):
        ref = ref or './config.yaml'
        if not os.path.exists(ref):
            raise NoConfigError('Config is not existed.')
        config_dict = load_ref(ref)
        self.config.update(config_dict)
        return config_dict

    def invoke_app(self):
        self.load_config()
        self.logger.info('Invoking app ...')
        for Component in self.components:
            self.logger.info('Invoke ' + Component.__name__ + '.')
            Component().invoke(self)
        self.logger.info('App has been invoked, the router list is:')
        self.pretty_url_map()
        return self

    def pretty_url_map(self):
        url_map = list(self.url_map.iter_rules())
        url_map.sort(key=attrgetter('rule'))
        pprint(url_map)


def create_app():
    app = App(__name__)

    app.use(RestFul)
    app.use(ErrorLog)

    return app
