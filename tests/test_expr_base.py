import pytest
import sys

from lessql.expr.base import Associativity, Precedence, State, state_factory


def test_associativity_order():
    assert Associativity.none < Associativity.left < Associativity.right


def test_precedence_default():
    p = Precedence()
    assert p.precedence == sys.maxint
    assert p.associativity == Associativity.none


def test_precedence_kwargs_construct():
    p = Precedence(associativity=Associativity.left, precedence=42)
    assert p.precedence == 42
    assert p.associativity == Associativity.left


def test_precedence_ordering():
    # More ordering tests are not needed since functools.total_ordering is used
    assert Precedence(42) < Precedence(9001)
    assert Precedence(42) < Precedence(42, Associativity.left)
    assert \
        Precedence(42, Associativity.left) < Precedence(42, Associativity.right)


def test_precedence_equality():
    assert not (
        Precedence(associativity=Associativity.left) ==
        Precedence(associativity=Associativity.right))
    assert \
        Precedence(associativity=Associativity.right) == \
        Precedence(associativity=Associativity.right)


def test_state_init():
    state = State(foo=u"bar", biz=u"baz")
    assert state.foo == u"bar"
    assert state.biz == u"baz"


def test_state_getattr():
    state = State(foo=u"bar")
    assert state.foo == u"bar"


def test_state_getattr_invalid():
    state = State(foo=u"bar")
    with pytest.raises(AttributeError):
        state.bar


def test_state_setattr():
    state = State()
    state.foo = u"bar"
    assert state.foo == u"bar"


def test_state_push_kwargs():
    state = State(foo=u"bar", biz=u"baz")
    assert state.foo == u"bar"
    assert state.biz == u"baz"

    state.push(foo=u"foobar")
    assert state.foo == u"foobar"
    assert state.biz == u"baz"


def test_state_push_arg():
    state = State(foo=[], bar=[])
    foo = state.foo
    bar = state.bar

    state.push("foo")
    state.foo.append(1)
    state.bar.append(1)

    assert state.foo is not foo
    assert state.bar is bar
    assert state.foo == [1]
    assert state.bar == [1]

    state.pop()
    assert state.foo is foo
    assert state.foo == []
    assert state.bar == [1]


def test_state_pop():
    state = State(foo=u"bar", biz=u"baz")
    state.push(foo=u"foobar")

    state.pop()
    assert state.foo == u"bar"
    assert state.biz == u"baz"


def test_state_with():
    state = State(foo=u"bar", biz=u"baz")

    with state(foo=u"foobar"):
        assert state.foo == u"foobar"
    assert state.foo == u"bar"


def test_state_parent():
    state = State(foo=u"bar", biz="baz")

    with state(foo=u"foobar"):
        assert state.parent.foo == u"bar"
        assert state.parent.biz == u"baz"


def test_state_len():
    state = State(foo=u"bar", biz="baz")
    assert len(state) == 1

    state.push()
    assert len(state) == 2

    state.push()
    assert len(state) == 3

    state.pop()
    assert len(state) == 2

    state.pop()
    assert len(state) == 1


def test_state_getall():
    state = State(foo=u"bar", biz=u"baz")
    assert list(state.getall(u"foo")) == [u"bar"]
    assert list(state.getall(u"biz")) == [u"baz"]

    with state(foo=u"foobar"):
        assert list(state.getall(u"foo")) == [u"foobar", u"bar"]
        assert list(state.getall(u"biz")) == [u"baz"]


def test_state_getall_missing():
    state = State(foo=u"bar", biz=u"baz")
    with state(foo=u"foobar"):
        assert list(state.getall(u"foo", missing=True)) == [u"foobar", u"bar"]
        assert list(state.getall(u"biz", missing=True)) == [None, u"baz"]


def test_state_getall_default():
    state = State(foo=u"bar", biz=u"baz")
    with state(foo=u"foobar"):
        assert list(state.getall(
            u"biz", missing=True, default=u"bizbaz")) == [u"bizbaz", u"baz"]

def test_default_state():
    state = state_factory()
    assert state.parameters == []
    assert state.precedence == Precedence(0)
