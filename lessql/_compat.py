"""
Compatibility module for Python 2 and 3.
"""

from abc import ABCMeta
from sys import version_info


__all__ = [
    "ChainMap",
    "python2",
    "add_metaclass",
    "bstr",
    "ustr",
    "string_type",
    "longint"
]


try:
    from collections import ChainMap
except ImportError:
    from chainmap import ChainMap


python2 = version_info.major == 2


def add_metaclass(metaclass):
    """
    Class decorator for creating a class with a metaclass. Shamelessly copied from
    Six (https://bitbucket.org/gutworth/six).

    .. code-block:: python

        @add_metaclass(MetaClass)
        def NormalClass(object):
            pass

    """

    def wrapper(cls):
        orig_vars = cls.__dict__.copy()
        slots = orig_vars.get("__slots__")

        if slots is not None:
            if isinstance(slots, str):
                slots = [slots]

            for slots_var in slots:
                orig_vars.pop(slots_var)

        orig_vars.pop("__dict__", None)
        orig_vars.pop("__weakref__", None)

        return metaclass(cls.__name__, cls.__bases__, orig_vars)
    return wrapper


# Python 2 compatibility for string types
if python2:
    bstr = str
    ustr = unicode
    string_type = basestring
    longint = long
else:
    bstr = bytes
    ustr = str

    @add_metaclass(ABCMeta)
    class string_type(object):
        pass

    string_type.register(str)
    string_type.register(bytes)

    longint = int

