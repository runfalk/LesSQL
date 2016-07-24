from .._compat import ustr, bstr, longint
from .base import compile

# Functions here are not intended to be used
__all__ = []

@compile.when(
    int, longint,
    bstr, ustr, # basestring is not used since this makes lookup faster
    bool, type(None))
def compile_builtins(compile, expr, state):
    state.parameters.append(expr)
    return u"?"

@compile.when(None)
def compile_none(compile, expr, state):
    return u"NULL"
