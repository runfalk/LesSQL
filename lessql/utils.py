import inspect

from collections import MutableMapping
from weakref import WeakValueDictionary

__all__ = [
    "ClassDict",
    "get_class",
]

class ClassDict(MutableMapping):
    """
    A dict implementation that uses classes as keys. If a sub class of a valid
    key is provided, the closest parent in the method resolution order is
    provided.

    The constructor accepts the same arguments as ``dict``.

    :param mapping_or_iterable: Mapping or iterable like the first argument of
                                ``dict()``.
    """

    def __init__(self, mapping_or_iterable=None):
        self.data = {}

        if mapping_or_iterable is None:
            return

        for k, v in dict(mapping_or_iterable).iteritems():
            self[k] = v

    def __getitem__(self, item):
        for cls in get_class(item).__mro__:
            if cls in self.data:
                return self.data[cls]

        raise KeyError(u"No data for class '{}'".format(
            get_class(item).__name__))

    def __setitem__(self, item, value):
        self.data[get_class(item)] = value

    def __delitem__(self, item):
        del self.data[get_class(item)]

    def __iter__(self):
        for item in self.data:
            yield item

    def __bool__(self):
        return bool(self.data)

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return '{0}({1!r})'.format(self.__class__.__name__, self.data)

    # Python 3 compatibility
    __nonzero__ = __bool__


def get_class(obj):
    """
    Get class of the given object. If given object is a class it is returned as
    is.

    :param obj: Class or instance to return class for
    :return: Class of object
    """

    return obj if inspect.isclass(obj) else obj.__class__
