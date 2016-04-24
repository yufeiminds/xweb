# -*- coding: utf-8 -*-

"""
xweb.utils
~~~~~~~~~~

Utilities definitions.
"""

import functools


class CachedProperty(object):
    ''' A property that is only computed once per instance and then replaces
        itself with an ordinary attribute. Deleting the attribute resets the
        property.
        See: https://github.com/bottlepy/bottle/commit/fa7733e075da0d790d809aa3d2f53071897e6f76
    '''

    def __init__(self, func):
        self.func = func

    def __get__(self, obj, cls):
        if obj is None: return self
        value = obj.__dict__[self.func.__name__] = self.func(obj)
        return value


cached_property = CachedProperty


def load_ref(ref):
    _top = None
    if ref.endswith('.json'):
        import json

        _top = json.load(ref)
    elif ref.endswith('.yaml'):
        import yaml

        _top = yaml.load(open(ref))
    return _top


def decorator(caller):
    " Implement like decorator.decorator "

    @functools.wraps(caller)
    def _deco(func):
        # Decorator generator.
        @functools.wraps(func)
        def _wraps(*args, **kwargs):
            return caller(func, *args, **kwargs)

        return _wraps

    return _deco