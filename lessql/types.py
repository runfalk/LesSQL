from .expr import Add, Subtract, Multiply, Divide, ComparableExpression

__all__ = [
    "SQLInt"
]

class SQLInt(ComparableExpression, int):
    pass
