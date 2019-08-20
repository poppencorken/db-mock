from .base import DBMock, DBMockConnection, StmtEntry
from .utils import _unpack_params, _normalize


class DBMockSyncConnection(DBMockConnection):
    def execute(self, query, params=None):
        _params = _unpack_params(query, params)
        _query = _normalize(query, self._dialect)
        self._seen_stmts.append(
            StmtEntry(query=query, params=_params, values=None, result=None)
        )

        expected = next(self._expected_stmts_iter)
        if _query == expected.query and _params == expected.params:
            return DBMockSyncCursor(expected.result)
        else:
            raise AssertionError("put in error message here")


class DBMockSync(DBMock):
    """Mocking class for blocking database access.

    Use it like this:

        mock = (DBMockAsync()
               .expect("SELECT * FROM users")
               .returns([(1, 'User 1'), (2, 'User 2')]))

        with mock as db:
            db.execute("SELECT * FROM admins")

    This example with throw an exception on exit of the with block because you
    didn't supply the correct select. If the query is not known at all to the
    mocking instance now value will be returned as well.

    """

    def __enter__(self):
        return DBMockSyncConnection(self._expected_stmts, self.dialect)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            raise


class DBMockSyncCursor(object):
    def __init__(self, result):
        self._closed = False
        self.result = result

    def __iter__(self):
        for entry in self.result["returns"]:
            self._check_closed()
            yield entry

    def _check_closed(self):
        if self._closed:
            raise IOError("Connection closed")

    @property
    def rowcount(self):
        self._check_closed()
        return self.result["rowcount"]

    def fetchall(self):
        self._check_closed()
        return list(self.result["returns"])

    def fetchmany(self, size=None):
        self._check_closed()

    def fetchone(self):
        self._check_closed()
        res = self.fetchall()
        if len(res) == 1:
            return res[0]
        else:
            raise RuntimeError("Result set didn't return exactly one row")

    def value(self):
        self._check_closed()
        row = self.fetchone()
        if len(row) == 1:
            return row[0]
        else:
            raise RuntimeError("Result set didn't return exactly one column")

    def close(self):
        self._closed = True
