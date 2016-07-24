from .base import Associativity, Precedence

class Expression(object):
    """
    Base class for all SQL expressions
    """

    __slots__ = ()
    precedence, associativity = Precedence()

class LateOperatorOverload(object):
    """
    Helper class for overloading operators at a later stage of execution
    """

    __slots__ = ()

    overload_map = {}

    # Arithmetic expressions
    def __add__(self, other):
        return self.perform(self, "add", other)

    def __sub__(self, other):
        return self.perform(self, "subract", other)

    def __mul__(self, other):
        return self.perform(self, "multiply", other)

    def __div__(self, other):
        return self.perform(self, "divide", other)

    def __mod__(self, other):
        return self.perform(self, "modulo", other)

    def __pow__(self, other):
        return self.perform(self, "power", other)

    def __radd__(self, other):
        return self.perform(other, "add", self)

    def __rsub__(self, other):
        return self.perform(other, "subtract", self)

    def __rmul__(self, other):
        return self.perform(other, "multiply", self)

    def __rdiv__(self, other):
        return self.perform(other, "divide", self)

    def __rmod__(self, other):
        return self.perform(other, "modulo", self)

    def __rpow__(self, other):
        return self.perform(other, "power", self)

    # Comparison expr.operators
    def __eq__(self, other):
        return self.perform(self, "equal", other)

    def __ne__(self, other):
        return self.perform(self, "not_equal", other)

    def __gt__(self, other):
        return self.perform(self, "greater_than", other)

    def __ge__(self, other):
        return self.perform(self, "greater_than_equal", other)

    def __lt__(self, other):
        return self.perform(self, "less_than", other)

    def __le__(self, other):
        return self.perform(self, "less_than_equal", other)

    def perform(self, left, operation, right):
        raise NotImplementedError("No perform operator defined")


def operator_mapping_factory(mapping=None):
    """
    Return a new LateOperatorOverload child class. This allows late binding of
    operators for many different classes.
    """

    if mapping is None:
        mapping = {}

    class OperatorMapping(LateOperatorOverload):
        overload_map = mapping

        @classmethod
        def map(cls, operation):
            def wrapper(func):
                cls.overload_map[operation] = func
                return func
            return wrapper

        def perform(self, left, operation, right):
            if operation not in self.overload_map:
                return NotImplemented
            return self.overload_map[operation](left, right)

    return OperatorMapping

Comparable = operator_mapping_factory()

class ComparableExpression(Comparable, Expression):
    __slots__ = ()
