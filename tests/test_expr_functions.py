import pytest

from lessql.expr import compile
from lessql.expr.functions import *


def test_compile_min(state):
    assert compile(Min(1, 2), state) == u"min(?, ?)"
    assert state.parameters == [1, 2]


def test_compile_max(state):
    assert compile(Max(1, 2), state) == u"max(?, ?)"
    assert state.parameters == [1, 2]


def test_compile_sqrt(state):
    assert compile(Sqrt(9), state) == u"sqrt(?)"
    assert state.parameters == [9]

    with pytest.raises(TypeError):
        Sqrt(1, 2)


def test_compile_power(state):
    assert compile(Power(2, 3), state) == u"power(?, ?)"
    assert state.parameters == [2, 3]

    with pytest.raises(TypeError):
        Power(1)

    with pytest.raises(TypeError):
        Power(1, 2, 3)
