import pytest
import sys

from lessql._compat import *
from lessql._compat import parent_getattr

def test_add_metaclass():
    class MetaRepr(type):
        def __repr__(cls):
            return "{}()".format(cls.__name__)

    @add_metaclass(MetaRepr)
    class Test(object):
        pass

    @add_metaclass(MetaRepr)
    class TestSlots(object):
        __slots__ = ()

    @add_metaclass(MetaRepr)
    class TestStrSlot(object):
        __slots__ = "foo"

    assert repr(Test) == "Test()"
    assert repr(TestSlots) == "TestSlots()"
    assert repr(TestStrSlot) == "TestStrSlot()"

def test_parent_getattr():
    class A(object):
        a = []

    class B(A):
        a = []
        b = []

    class C(B):
        b = []
        c = []

    assert parent_getattr(B, "a") is A.a
    assert parent_getattr(B, "b") is None

    assert parent_getattr(C, "a") is B.a
    assert parent_getattr(C, "b") is B.b
    assert parent_getattr(C, "c") is None


@pytest.mark.skipif(not python2, reason="Python 2 specific test")
def test_python2_rewrite_magic_methods_str():
    unicode_atom = u"unicode"

    @rewrite_magic_methods
    class Unicode(object):
        def __str__(self):
            return unicode_atom

    assert Unicode().__unicode__() is unicode_atom


@pytest.mark.skipif(not python2, reason="Python 2 specific test")
def test_python2_rewrite_magic_methods_bytes():
    bytes_atom = b"unicode"

    @rewrite_magic_methods
    class Bytes(object):
        def __bytes__(self):
            return bytes_atom

    assert Bytes().__str__() is bytes_atom
    assert not hasattr(Bytes(), "__bytes__")


@pytest.mark.skipif(not python2, reason="Python 2 specific test")
def test_python2_rewrite_magic_methods_str_bytes():
    unicode_atom = u"unicode"
    bytes_atom = b"unicode"

    @rewrite_magic_methods
    class Str(object):
        def __str__(self):
            return unicode_atom

        def __bytes__(self):
            return bytes_atom

    assert Str().__unicode__() is unicode_atom
    assert Str().__str__() is bytes_atom
    assert not hasattr(Str(), "__bytes__")


@pytest.mark.skipif(not python2, reason="Python 2 specific test")
def test_python2_rewrite_magic_methods_bool():
    bytes_atom = b"unicode"

    @rewrite_magic_methods
    class Bool(object):
        def __bool__(self):
            return False

    assert Bool().__nonzero__() is False
    assert not hasattr(Bool(), "__bool__")


def test_bstr():
    assert type(b"") is bstr


def test_ustr():
    assert type(u"") is ustr


def test_string_type():
    assert isinstance(b"", string_type)
    assert isinstance(u"", string_type)

def test_longint():
    assert isinstance(sys.maxsize + 1, longint)
