import pytest

from lessql.expr.base import compile, state_factory
from lessql.expr.operators import *


@pytest.mark.parametrize("expr, sql, params", [
    (UnaryPlus(1), u"+?", [1]),
    (UnaryMinus(1), u"-?", [1]),
    (Not(1), u"NOT ?", [1]),
    (Add(1, 2), u"? + ?", [1, 2]),
    (Subtract(1, 2), u"? - ?", [1, 2]),
    (Multiply(1, 2), u"? * ?", [1, 2]),
    (Divide(1, 2), u"? / ?", [1, 2]),
    (Modulo(1, 2), u"? % ?", [1, 2]),
    (In(1, 2), u"? IN ?", [1, 2]),
    (Is(1, 2), u"? IS ?", [1, 2]),
    (IsNot(1, 2), u"? IS NOT ?", [1, 2]),
    (Equal(1, 2), u"? = ?", [1, 2]),
    (NotEqual(1, 2), u"? != ?", [1, 2]),
    (GreaterThan(1, 2), u"? > ?", [1, 2]),
    (GreaterThanEqual(1, 2), u"? >= ?", [1, 2]),
    (LessThan(1, 2), u"? < ?", [1, 2]),
    (LessThanEqual(1, 2), u"? <= ?", [1, 2]),
    (And(1, 2), u"? AND ?", [1, 2]),
    (Or(1, 2), u"? OR ?", [1, 2]),
])
def test_operator(expr, sql, params, state):
    assert compile(expr, state) == sql
    assert state.parameters == params


def test_equal_is_when_none(state):
    assert compile(Equal(1, None), state) == u"? IS NULL"
    assert state.parameters == [1]


def test_not_equal_is_when_none(state):
    assert compile(NotEqual(1, None), state) == u"? IS NOT NULL"
    assert state.parameters == [1]


@pytest.mark.parametrize("expr, precedence", [
    (UnaryPlus, 1100),
    (UnaryMinus, 1100),
    (Multiply, 900),
    (Divide, 900),
    (Modulo, 900),
    (Add, 800),
    (Subtract, 800),
    (Operator, 700), # Default operator precedence
    (NotEqual, 700),
    (In, 600),
    (NotIn, 600),
    (Equal, 500),
    (GreaterThan, 500),
    (GreaterThanEqual, 500),
    (LessThan, 500),
    (LessThanEqual, 500),
    (Is, 400),
    (IsNot, 400),
    (Not, 300),
    (And, 200),
    (Or, 100),
])
def test_precedence(expr, precedence):
    assert expr.precedence == precedence


@pytest.mark.parametrize("expr, associativity", [
    (UnaryPlus, Associativity.right),
    (UnaryMinus, Associativity.right),
    (Multiply, Associativity.left),
    (Divide, Associativity.left),
    (Modulo, Associativity.left),
    (Add, Associativity.left),
    (Subtract, Associativity.left),
    (Operator, Associativity.left), # Default operator associativity
    (NotEqual, Associativity.left),
    (In, Associativity.none),
    (NotIn, Associativity.none),
    (Equal, Associativity.none),
    (GreaterThan, Associativity.none),
    (GreaterThanEqual, Associativity.none),
    (LessThan, Associativity.none),
    (LessThanEqual, Associativity.none),
    (Is, Associativity.none),
    (IsNot, Associativity.none),
    (Not, Associativity.right),
    (And, Associativity.left),
    (Or, Associativity.left),
])
def test_associativity(expr, associativity):
    assert expr.associativity is associativity


@pytest.mark.parametrize("cls, rep", [
    (UnaryPlus, u'UnaryPlus("+")'),
    (UnaryMinus, u'UnaryMinus("-")'),
    (Not, u'Not("NOT")'),
    (Add, u'Add("+")'),
    (Subtract, u'Subtract("-")'),
    (Multiply, u'Multiply("*")'),
    (Divide, u'Divide("/")'),
    (Modulo, u'Modulo("%")'),
    (In, u'In("IN")'),
    (NotIn, u'NotIn("NOT IN")'),
    (Is, u'Is("IS")'),
    (IsNot, u'IsNot("IS NOT")'),
    (Equal, u'Equal("=")'),
    (NotEqual, u'NotEqual("!=")'),
    (GreaterThan, u'GreaterThan(">")'),
    (GreaterThanEqual, u'GreaterThanEqual(">=")'),
    (LessThan, u'LessThan("<")'),
    (LessThanEqual, u'LessThanEqual("<=")'),
    (And, u'And("AND")'),
    (Or, u'Or("OR")'),
])
def test_repr(cls, rep):
    assert repr(cls) == rep

def test_repr_undefined_operator():
    assert repr(Operator) == u"Operator()"
