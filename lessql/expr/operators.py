"""
LesSQL operator module
----------------------
LesSQL automatically puts brackets around expressions when needed. The internal
precedence table is based on `PostgreSQL 9.5
<https://www.postgresql.org/docs/9.5/static/sql-syntax-lexical.html#SQL-PRECEDENCE>`_.

==========  =============  =========
Precedence  Associativity  Operators
==========  =============  =========
1400        left           ``.``
1300        left           ``::``
1200        left           ``[``, ``]``
1100        right          ``+``, ``-`` (unary)
1000        left           ``^``
900         left           ``*``, ``/``, ``%``
800         left           ``+``, ``-`` (binary)
700         left           (any other operator)
600                        ``BETWEEN``, ``IN``, ``LIKE``, ``ILIKE``, ``SIMILAR`
500                        ``<``, ``>``, ``=``, ``<=``, ``>=``, ``<>``
400                        ``IS``, ``ISNULL``, ``NOTNULL`` (all IS x expressions)
300         right          ``NOT``
200         left           ``AND``
100         left           ``OR``
==========  =============  =========
"""

from collections import namedtuple
from functools import wraps

from .base import compile, Associativity
from .common import ComparableExpression, Comparable


__alla__ = [
    "Operator",
    "UnaryOperator",
    "UnaryPlus",
    "UnaryMinus",
    "Not",
    "BinaryOperator",
]

class MetaOperator(type):
    def __repr__(self):
        if self.operator is None:
            return '{0.__name__}()'.format(self)
        else:
            return '{0.__name__}("{1}")'.format(self, self.operator.strip())


class Operator(ComparableExpression):
    __metaclass__ = MetaOperator

    __slots__ = ()
    operator = None

    # Default precedence
    precedence = 700

    # Default associativity
    associativity = Associativity.left


class UnaryOperator(Operator):
    __slots__ = ("operand",)
    associativity = Associativity.right

    def __init__(self, operand):
        self.operand = operand

@compile.when(UnaryOperator)
def compile_unary_operator(compile, expr, state):
    return u"{}{}".format(expr.operator, compile(expr.operand, state))


class UnaryPlus(UnaryOperator):
    __slots__ = ()
    operator = "+"
    precedence = 1100


class UnaryMinus(UnaryOperator):
    __slots__ = ()
    operator = "-"
    precedence = 1100


class Not(UnaryOperator):
    __slots__ = ()
    operator = "NOT "
    precedence = 300


class BinaryOperator(Operator):
    __slots__ = ("left", "right")

    def __init__(self, left, right):
        self.left = left
        self.right = right

@compile.when(BinaryOperator)
def compile_binary_operator(compile, expr, state):
    left = compile(expr.left, state)
    right = compile(expr.right, state)

    return u"{} {} {}".format(left, expr.operator, right)

# Arithmetic operators
@Comparable.map("add")
class Add(BinaryOperator):
    __slots__ = ()
    operator = u"+"
    precedence = 800


@Comparable.map("subtract")
class Subtract(BinaryOperator):
    __slots__ = ()
    operator = u"-"
    precedence = 800


@Comparable.map("multiply")
class Multiply(BinaryOperator):
    __slots__ = ()
    operator = u"*"
    precedence = 900

@Comparable.map("divide")
class Divide(BinaryOperator):
    __slots__ = ()
    operator = u"/"
    precedence = 900


@Comparable.map("modulo")
class Modulo(BinaryOperator):
    __slots__ = ()
    operator = u"%"
    precedence = 900


# Containment operators
class In(BinaryOperator):
    __slots__ = ()
    operator = u"IN"
    precedence = 600
    associativity = Associativity.none

class NotIn(BinaryOperator):
    operator = u"NOT IN"
    precedence = 600
    associativity = Associativity.none

# Comparison operators
class Is(BinaryOperator):
    __slots__ = ()
    operator = u"IS"
    precedence = 400
    associativity = Associativity.none


class IsNot(BinaryOperator):
    __slots__ = ()
    operator = "IS NOT"
    precedence = 400
    associativity = Associativity.none


@Comparable.map("equal")
class Equal(BinaryOperator):
    __slots__ = ()
    operator = u"="
    precedence = 500
    associativity = Associativity.none

@compile.when(Equal)
def compile_equal(compile, expr, state):
    # Rewrite expressions when comparing to None. This is necessary since it is
    # not possible to overload the is operator in Python.
    if expr.right is None:
        # Make outer state available to ensure proper bracket use by using outer
        # precedence and associativity.
        with state.parent() as outer_state:
            return compile(Is(expr.left, expr.right), outer_state)
    else:
        new_expr = BinaryOperator(expr.left, expr.right)
        new_expr.operator = "="

        return compile(new_expr, state)


@Comparable.map("not_equal")
class NotEqual(BinaryOperator):
    __slots__ = ()
    operator = u"!="
    precedence = 700

@compile.when(NotEqual)
def compile_not_equal(compile, expr, state):
    # Rewrite expressions when comparing to None. This is necessary since it is
    # not possible to overload the is operator in Python.
    if expr.right is None:
        # Make outer state available to ensure proper bracket use by using outer
        # precedence and associativity.
        with state.parent() as outer_state:
            return compile(IsNot(expr.left, expr.right), outer_state)
    else:
        new_expr = BinaryOperator(expr.left, expr.right)
        new_expr.operator = "!="

        return compile(new_expr, state)


@Comparable.map("greater_than")
class GreaterThan(BinaryOperator):
    __slots__ = ()
    operator = u">"
    precedence = 500
    associativity = Associativity.none


@Comparable.map("greater_than_equal")
class GreaterThanEqual(BinaryOperator):
    __slots__ = ()
    operator = u">="
    precedence = 500
    associativity = Associativity.none


@Comparable.map("less_than")
class LessThan(BinaryOperator):
    __slots__ = ()
    operator = u"<"
    precedence = 500
    associativity = Associativity.none


@Comparable.map("less_than_equal")
class LessThanEqual(BinaryOperator):
    __slots__ = ()
    operator = u"<="
    precedence = 500
    associativity = Associativity.none


class ComparableOperator(Operator):
    __slots__ = ("exprs",)
    associativity = Associativity.left

    def __init__(self, *exprs):
        self.exprs = exprs


@compile.when(ComparableOperator)
def compile_comparable_operator(compile, expr, state):
    return u" {} ".format(expr.operator).join(
        compile(e, state) for e in expr.exprs)


class And(ComparableOperator):
    __slots__ = ()
    operator = u"AND"
    precedence = 200


class Or(ComparableOperator):
    __slots__ = ()
    operator = u"OR"
    precedence = 100
