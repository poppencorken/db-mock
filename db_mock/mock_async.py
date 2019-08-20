from typing import List

from db_mock.base import DBMock, DBMockConnection, StmtEntry
from db_mock.utils import _normalize, _unpack_params


class DBMockAsyncConnection(DBMockConnection):
    async def execute(
        self, query, params: dict = None, values: List[dict] = None
    ):
        _params = _unpack_params(query, params)
        _query = _normalize(query, self._dialect)
        self._seen_stmts.append(
            StmtEntry(query=query, params=_params, values=None, result=None)
        )

        expected = next(self._expected_stmts_iter)
        if (
            _query == expected.query
            and _params == expected.params
            and values == expected.values
        ):
            return expected.result["returns"]
        else:
            raise Exception

    async def fetch_all(self, query, params: dict = None):
        return await self.execute(query, params)

    async def fetch_one(self, query, params: dict = None):
        result = await self.fetch_all(query, params)
        if len(result) == 1:
            return result[0]
        else:
            raise RuntimeError("Not exactly one row returned.")

    async def fetch_val(self, query, params: dict = None):
        row = await self.fetch_one(query, params=params)
        if len(row) == 1:
            return row[0]
        else:
            raise RuntimeError("Not exactly one column returned.")

    async def execute_many(self, query, values: List[dict] = None):
        return await self.execute(query, values=values)

    async def iterate(self, query, params: dict = None):
        pass


class DBMockAsync(DBMock):
    async def __aenter__(self):
        return DBMockAsyncConnection(self._expected_stmts, self.dialect)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            raise
