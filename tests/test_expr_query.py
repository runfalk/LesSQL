import pytest

from lessql.expr import compile, Add
from lessql.expr.query import Select, Table

def test_select_minimal(state):
    ast = Select(columns=[Add(1, 2)])
    assert compile(ast, state) == u"SELECT ? + ?"
    assert state.parameters == [1, 2]


def test_select_table(state):
    ast = Select(tables=[Table(u"table")])
    assert compile(ast, state) == u"SELECT * FROM table"
    assert state.parameters == []
