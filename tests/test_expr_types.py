import pytest
import sys

from lessql._compat import python2
from lessql.expr import compile


@pytest.mark.parametrize("param", [
    1,
    sys.maxint + 1,
    b"foobar",
    u"foobar",
    True,
    False,
])
def test_compile_builtin(state, param):
    assert compile(param, state) == u"?"
    assert state.parameters == [param]


def test_compile_none(state):
    assert compile(None, state) == u"NULL"
    assert state.parameters == []
