import pytest
import operator

from lessql.expr.common import LateOperatorOverload, operator_mapping_factory
from mock import Mock


def test_perform_not_implemented_error():
    with pytest.raises(NotImplementedError):
        LateOperatorOverload() + 1


@pytest.mark.parametrize("name, operation", [
    (u"add", operator.add),
    (u"subtract", operator.sub),
    (u"multiply", operator.mul),
    (u"divide", operator.div),
    (u"modulo", operator.mod),
    (u"power", operator.pow),
    (u"equal", operator.eq),
    (u"not_equal", operator.ne),
    (u"greater_than", operator.gt),
    (u"greater_than_equal", operator.ge),
    (u"less_than", operator.lt),
    (u"less_than_equal", operator.le),
])
def test_late_operator_overload_operators(name, operation):
    class OperatorMapping(LateOperatorOverload):
        def perform(self, left, operation, right):
            assert left is self
            assert right is None
            assert operation == name

    operation(OperatorMapping(), None)


@pytest.mark.parametrize("name, operation", [
    (u"add", operator.add),
    (u"subtract", operator.sub),
    (u"multiply", operator.mul),
    (u"divide", operator.div),
    (u"modulo", operator.mod),
    (u"power", operator.pow),
])
def test_late_operator_overload_reverse_operators(name, operation):
    class OperatorMapping(LateOperatorOverload):
        def perform(self, left, operation, right):
            assert left is None
            assert right is self
            assert operation == name

    operation(None, OperatorMapping())


def test_operator_mapping_factory_bases():
    OperatorMapping = operator_mapping_factory()
    assert issubclass(OperatorMapping, LateOperatorOverload)


def test_operator_mappning_factory_map():
    class A(operator_mapping_factory()):
        pass

    mock = A.map("add")(Mock())
    assert not mock.called

    with pytest.raises(TypeError):
        A() - None
    assert not mock.called

    A() + None
    assert mock.called
