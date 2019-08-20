import pytest
import sqlalchemy as sa

from db_mock import DBMockSync
from db_mock.utils import _normalize


QUERIES = [
    "select * from users",
    sa.select([sa.literal_column("*")]).select_from(sa.table("users")),
]


@pytest.fixture(params=QUERIES)
def query(request):
    return request.param


def test_normalize(query):
    import sqlalchemy.engine.default as default

    assert _normalize(query, default.DefaultDialect()) == (
        """SELECT *
FROM users"""
    )


def test_blocking(query):
    mock = (
        DBMockSync()
        .expect_stmt(query)
        .expect_returns([(1, "User 1"), (2, "User 2")])
        .expect_stmt("update users set password = 'hunter1' where id = 1;")
        .expect_rowcount(1)
        .expect_stmt("select count(*) from users")
        .expect_returns([(5,)])
        .expect_stmt("delete from users where id = :id", {"id": 1})
        .expect_rowcount(1)
        .expect_stmt(query)
        .expect_returns([(2, "User 2")])
    )

    with mock as db:
        for count, user in enumerate(
            db.execute(query), start=1
        ):
            assert count == user[0]
            assert user[1].startswith("User")

        upd = db.execute("update users set password = 'hunter1' where id = 1")
        assert upd.rowcount == 1

        upd = db.execute("select count(*) from users").value()
        assert upd == 5

        res = db.execute("delete from users where id = :id", {"id": 1})
        assert res.rowcount == 1

        res = db.execute(query).fetchone()
        assert res[0] == 2


def test_failing(query):
    mock = (
        DBMockSync()
        .expect_stmt(query)
        .expect_returns([(1, "User 1"), (2, "User 2")])
        .expect_stmt("update users set password = 'hunter1' where id = 1;")
        .expect_rowcount(1)
        .expect_stmt("select count(*) from users")
        .expect_returns([(5,)])
        .expect_stmt("delete from users where id = 1")
        .expect_rowcount(1)
        .expect_stmt(query)
        .expect_returns([(2, "User 2")])
    )
