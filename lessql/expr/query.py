from .base import compile
from .common import Expression, ComparableExpression

# WIP
__all__ = [
    "Select",
]

class Table(Expression):
    __slots__ = ("name")

    def __init__(self, name):
        self.name = name

@compile.when(Table)
def compile_table(compile, expr, state):
    # TODO: Fix this
    return expr.name

class TableExpression(Table):
    __slots__ = ("name",)

    def column(self, name):
        pass


class Column(ComparableExpression):
    __slots__ = ("name", "table")

    def __init__(self, name, table=None):
        self.name = name
        self.table = table

    def get_table(self):
        return Table(self.table)


class Alias(Column):
    pass


class Window(object):
    # https://www.postgresql.org/docs/9.0/static/sql-select.html#SQL-WINDOW
    pass


class Select(Expression):
    # https://www.postgresql.org/docs/9.0/static/sql-select.html#SQL-SELECT
    __slots__ = (
        "columns",
        "tables",
        "where",
        "group_by",
        "having",
        "order_by",
        "limit",
        "offset",
        "distinct",
        "window",
        "with_",
    )
    precedence = 0

    def __init__(
            self, columns=None, tables=None, where=None, group_by=None,
            having=None, order_by=None, limit=None, offset=None, distinct=None,
            with_=None, window=None):
        self.columns = columns
        self.tables = tables
        self.where = where
        self.group_by = group_by
        self.having = having
        self.order_by = order_by
        self.limit = limit
        self.offset = offset
        self.distinct = distinct
        self.window = window
        self.with_ = with_


@compile.when(Select)
def compile_select(compile, expr, state):
    tokens = []

    # TODO: Handle with statements, self.with_

    tokens.append(u"SELECT")
    if expr.columns is None:
        tokens.append("*")
    else:
        tokens.append(u", ".join(compile(col, state) for col in expr.columns))

    # TODO: Automatically infer tables
    if expr.tables is not None:
        tokens.append(u"FROM")
        tokens.append(u", ".join(compile(table, state) for table in expr.tables))

    # TODO: Do not allow where, etc if there are no tables

    if expr.where is not None:
        tokens.append(u"WHERE")
        tokens.append(compile(expr.where, state))

    if expr.group_by is not None:
        tokens.append(u"GROUP BY")
        tokens.append(u", ".join(compile(expr, state) for expr in expr.group_by))

    if expr.having is not None:
        tokens.append(u"HAVING")
        tokens.append(compile(expr.where, state))

    if expr.window is not None:
        # TODO: Implement window
        #tokens.append(u"WINDOW")
        #tokens.append(compile(, state))
        pass

    if expr.order_by is not None:
        tokens.append(u"GROUP BY")
        tokens.append(u", ".join(compile(expr, state) for expr in expr.order_by))

    if expr.limit is not None:
        tokens.append(u"LIMIT {:d}".format(expr.limit))

    if expr.offset is not None:
        tokens.append(u"OFFSET {:d}".format(expr.offset))

    return u" ".join(tokens)

class Update(object):
    pass

class Insert(object):
    pass

class Replace(object):
    pass



class SetExpression(object):
    __slots__ = ("left", "right")

    operation = None

    def __init__(self, left, right):
        self.left = left
        self.right = right

@compile.when(SetExpression)
def compile_set_expression(compile, expr, state):
    return u"{left} {operation} {right}".format(
        left=compile(expr.left, state),
        operation=expr.operation,
        right=compile(expr.right, state))

class Union(SetExpression):
    __slots__ = ()
    operation = "UNION"

class Intersect(SetExpression):
    __slots__ = ()
    operation = "INTERSECT"

class Except(SetExpression):
    __slots__ = ()
    operation = "EXCEPT"
