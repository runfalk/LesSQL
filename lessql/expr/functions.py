from .base import compile
from .common import Expression

__all__ = [
    "Function",
    "Min",
    "Max",
    "Sqrt",
    "Power",
]

class Function(Expression):
    __slots__ = ("args",)
    name = None

    def __init__(self, *args):
        self.args = args

@compile.when(Function)
def compile_function(compile, expr, state):
    return u"{}({})".format(expr.name, u", ".join(
        compile(arg, state) for arg in expr.args))


class Min(Function):
    __slots__ = ()
    name = "min"


class Max(Function):
    __slots__ = ()
    name = u"max"


class Sqrt(Function):
    __slots__ = ()
    name = u"sqrt"

    def __init__(self, x):
        super(Sqrt, self).__init__(x)


class Power(Function):
    __slots__ = ()
    name = u"power"

    def __init__(self, x, y):
        super(Power, self).__init__(x, y)
