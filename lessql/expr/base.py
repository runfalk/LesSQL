import sys

from collections import namedtuple
from contextlib import contextmanager
from copy import copy
from enum import Enum
from functools import total_ordering
from itertools import chain

from .._compat import ChainMap
from ..utils import get_class, ClassDict


class OrderedEnum(Enum):
    """
    Provide ordering for enums.

    By default enums are only comparable for equality. This sub-class allow
    comparison operators to be used.

    Shamelessly copied from the `python documentation
    <https://docs.python.org/3/library/enum.html#orderedenum>`_
    """

    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented
    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented
    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


class Associativity(OrderedEnum):
    """
    A special enum type for operator associativity. Unlike normal enums this one
    supports orderings for its attributes.
    """

    #: For operators with no associativity
    none = 0

    #: For left-associative operators
    left = 1

    #: For right-associative operators
    right = 2


class Context(Enum):
    #: The default context for compilation
    none = 0

    #: Context when compiling an expression as a column
    column = 1

    #: Context when compiling an expression as a table
    table = 2


@total_ordering
class Precedence(namedtuple("_Precedence", ["precedence", "associativity"])):
    """
    Named tuple containing precedence and associativity. It implements
    comparison operators which means precedence can be easily determined by
    calling code.

    :param precedence: Expression precedence as an int.
    :param associatity: Expression associativity as an enum value as defined in
                        :class:`Associativity`.
    """

    __slots__ = ()

    def __new__(cls, precedence=None, associativity=None):
        return super(Precedence, cls).__new__(
            cls,
            sys.maxint if precedence is None else precedence,
            Associativity.none if associativity is None else associativity)

    def __repr__(self):
        parent_repr = super(Precedence, self).__repr__()
        return self.__class__.__name__ + "(" + parent_repr.split("(", 1)[1]

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self[0] == other[0] and self[1] == other[1]

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.precedence < other.precedence or
            self.precedence == other.precedence and
            self.associativity < other.associativity)


class Compiler(object):
    """
    Translates AST into SQL strings.

    Constructor should not be called directly.

    :param parent: A Compiler instance to inherit compilation rules from
    """

    _default_precedence = Precedence()

    def __init__(self, parent=None):
        self.parent = parent
        self._map = ClassDict()

    def when(self, *classes):
        def decorator(func):
            for cls in classes:
                self._map[cls] = func
        return decorator

    def _get_precedence(self, cls):
        return Precedence(
            getattr(cls, "precedence", self._default_precedence.precedence),
            getattr(cls, "associativity", self._default_precedence.associativity))

    def __call__(self, expr, state=None):
        if state is None:
            state = state_factory()

        precedence = self._get_precedence(expr)
        with state(precedence=precedence):
            compiled = self._map[expr](self, expr, state)

        if precedence < state.precedence:
            return u"({})".format(compiled)
        return compiled


#: Default compiler
compile = Compiler()


class State(object):
    __slots__ = ("_state")
    Undef = type("Undef", (), {})()

    def __init__(self, *args, **kwargs):
        # Prevent __setattr__ from intercepting _state
        super(State, self).__setattr__(
            "_state", ChainMap(dict(*args, **kwargs)))

    @property
    def parent(self):
        parent = self.__class__.__new__(self.__class__)
        super(State, parent).__setattr__("_state", self._state.parents)
        return parent

    def getall(self, attr, missing=None, default=None):
        if missing is None:
            missing = False

        return (
            d.get(attr, default)
            for d in self._state.maps if missing or attr in d)

    def compact(self):
        """
        Create a new dictionary for the current state context. This does not
        make any copies of objects.

        :returns: A new dictionary containing all attributes and values
                  associated with the current state.
        """

        return {k: v for k, v in self._state.items()}

    def push(self, *args, **kwargs):
        if args:
            mapping = [(attr, copy(self._state[attr])) for attr in args]
        else:
            mapping = []

        super(State, self).__setattr__(
            "_state", self._state.new_child(dict(mapping, **kwargs)))

    def pop(self):
        super(State, self).__setattr__("_state", self._state.parents)

    @contextmanager
    def __call__(self, *args, **kwargs):
        self.push(*args, **kwargs)
        yield self
        self.pop()

    def __getattr__(self, attr):
        try:
            return self._state[attr]
        except KeyError:
            raise AttributeError(u"type object '{}' has no attribute '{}'".format(
                self.__class__.__name__, attr))

    def __setattr__(self, attr, value):
        try:
            # Check if attribute exists on instance directly. This allows us to
            # assign directly to self._state.
            super(State, self).__getattr__(attr)
        except AttributeError:
            self._state[attr] = value
        else:
            super(State, self).__setattr__(attr, value)

    def __len__(self):
        return len(self._state.maps)

    def __repr__(self):
        return '{0.__class__.__name__}({1!r})'.format(
            self, dict(self._state.items()))


def state_factory(*args, **kwargs):
    state = State(
        precedence=Precedence(0),
        parameters=[])
    state.push(*args, **kwargs)

    return state
