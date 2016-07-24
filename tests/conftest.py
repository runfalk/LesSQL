import pytest

from lessql.expr import state_factory

@pytest.fixture
def state():
    return state_factory()
