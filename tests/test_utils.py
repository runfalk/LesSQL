import pytest

from collections import MutableMapping
from lessql.utils import ClassDict, get_class


class A(object):
    pass


class B(A):
    pass


class C(A):
    pass


class D(B):
    pass


def test_class_dict_constructor():
    ClassDict()
    ClassDict({})
    ClassDict([])
    ClassDict({A: None, D: None})
    ClassDict([(A, None), (C, None)])


def test_class_dict_invalid_constructor():
    with pytest.raises(TypeError):
        ClassDict(1)

    with pytest.raises(TypeError):
        ClassDict(False)

    with pytest.raises(TypeError):
        ClassDict([A, None])

    with pytest.raises(ValueError):
        ClassDict("foobar")


def test_get_direct_key():
    d = ClassDict({
        A: "a",
        D: "d",
    })

    assert d[A] == "a"
    assert d[D] == "d"


def test_get_indirect_key():
    d = ClassDict({
        A: "a",
        C: "c",
    })

    assert d[A] == "a"
    assert d[B] == "a"
    assert d[D] == "a"
    assert d[C] == "c"


@pytest.mark.parametrize("key", [A, B, D])
def test_get_missing_key(key):
    d = ClassDict({C: "c"})
    with pytest.raises(KeyError):
        d[key]


def test_set_item():
    d = ClassDict({B: "b"})

    assert d[B] == "b"
    assert d[D] == "b"

    d[D] = "d"
    assert d[B] == "b"
    assert d[D] == "d"

def test_replace_item():
    d = ClassDict()

    d[A] = "a"
    assert d[A] == "a"

    d[A] = "A"
    assert d[A] == "A"


def test_delete_item():
    d = ClassDict({B: "b"})

    assert d[B] == "b"
    del d[B]

    with pytest.raises(KeyError):
        del d[B]


@pytest.mark.parametrize("key", [B, C, D])
def test_delete_indirect_item(key):
    d = ClassDict({A: "a"})
    with pytest.raises(KeyError):
        del d[key]


def test_iter():
    data = {A: "a", B: "b"}
    d = ClassDict(data)

    assert set(d.items()) == set(data.items())


def test_len():
    d = ClassDict()
    assert len(d) == 0

    d[A] = "a"
    assert len(d) == 1

    d[C] = "c"
    assert len(d) == 2

    d[D] = "d"
    assert len(d) == 3


def test_repr():
    d = ClassDict()
    assert repr(d) == "ClassDict({})"

    data = {A: None}
    d = ClassDict(data)
    assert repr(d) == "ClassDict({!r})".format(data)

    data = {A: None, B: None}
    d = ClassDict(data)
    assert repr(d) == "ClassDict({!r})".format(data)


def test_bool():
    d = ClassDict()
    assert not d

    d[A] = None
    assert d


def test_sub_classing():
    assert isinstance(ClassDict(), MutableMapping)


def test_get_class():
    assert get_class(A) is A
    assert get_class(D) is D


def test_get_class_from_instance():
    assert get_class(A()) is A
    assert get_class(D()) is D
