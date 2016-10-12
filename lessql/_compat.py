"""
Compatibility module for Python 2 and 3.
"""

from abc import ABCMeta
from sys import version_info


__all__ = [
    "ChainMap",
    "is_python2",
    "add_metaclass",
    "rewrite_magic_methods",
    "bstr",
    "ustr",
    "string_type",
    "longint"
]


# Use Python's own ChainMap implementation when it is available, otherwise fall
# back on backport. Other modules should import ChainMap from here instead of
# performing the check in that module.
try:
    from collections import ChainMap
except ImportError:
    from chainmap import ChainMap


is_python2 = version_info.major == 2


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


def parent_getattr(cls, attr, default=None):
    for parent in cls.__bases__:
        if hasattr(parent, attr):
            return getattr(parent, attr, default)
    return default


def rewrite_magic_methods(cls):
    if is_python2:
        # Create a unique value that we use to test if methods are defined
        Undef = type("Undef", (), {})()

        cls_str = getattr(cls, "__str__", Undef)
        cls_bytes = getattr(cls, "__bytes__", Undef)
        cls_bool = getattr(cls, "__bool__", Undef)

        parent_str = parent_getattr(cls, "__str__", Undef)
        parent_bytes = parent_getattr(cls, "__bytes__", Undef)
        parent_bool = parent_getattr(cls, "_)_bool__", Undef)

        # Check if class has attribute/method and that it is different from the
        # parent's value if it exists.
        has_str = cls_str is not Undef and cls_str is not parent_str
        has_bytes = cls_bytes is not Undef and cls_bytes is not parent_bytes
        has_bool = cls_bool is not Undef and cls_bool is not parent_bool

        if has_str and has_bytes:
            cls.__unicode__, cls.__str__ = cls_str, cls_bytes
            delattr(cls, "__bytes__")
        elif has_str:
            cls.__unicode__ = cls_str
            delattr(cls, "__str__")
        elif has_bytes:
            cls.__str__ = cls_bytes
            delattr(cls, "__bytes__")

        if has_bool:
            print cls_bool, parent_bool
            cls.__nonzero__ = cls_bool
            delattr(cls, "__bool__")

    return cls


# Python 2 compatibility for string types
if is_python2:
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

