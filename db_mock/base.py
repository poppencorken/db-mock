"""
TODO

 [X] async implementation
 [ ] test failing cases
 [ ] better error messages
 [ ] latency support
 [ ] write mkdocs docs
 [ ] read the docs integration
 [W] py2 async import warnings

"""
import collections

from .utils import _unpack_params, _normalize


class DBMockConnection(object):
    def __init__(self, expected_stmts, dialect):
        self._dialect = dialect
        self._expected_stmts_iter = iter(expected_stmts)
        self._seen_stmts = []


class DBMock(object):
    def __init__(self, dialect=None):
        self.dialect = dialect
        self.is_connected = False
        self._expected_stmts_iter = None
        self._expected_stmts = []

    def expect_stmt(self, query, params=None, values=None):
        self._expected_stmts.append(
            StmtEntry(
                query=_normalize(query, self.dialect),
                params=_unpack_params(query, params),
                values=values,
                result={},
            )
        )
        return self

    def expect_rowcount(self, count):
        return self.expect_result(rowcount=count)

    def expect_returns(self, returns):
        return self.expect_result(returns=returns)

    def expect_result(self, returns=None, rowcount=None):
        if not self._expected_stmts:
            raise RuntimeError(
                "expect_result() called before any statements added. "
                "Call expect_stmt() method first."
            )
        current_stmt = self._expected_stmts[-1]
        if not current_stmt.result:
            current_stmt.result.update(
                {"returns": returns, "rowcount": rowcount}
            )
        else:
            raise RuntimeError(
                "expect_result() may only be called once per statement."
            )
        return self


StmtEntry = collections.namedtuple(
    "StmtResult", ["query", "params", "values", "result"]
)
