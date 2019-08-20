import pytest

from db_mock import DBMockAsync


@pytest.mark.asyncio
async def test_async_execute():
    mock = (
        DBMockAsync()
        .expect_stmt("select * from users")
        .expect_returns([(1, "User 1"), (2, "User 2")])
        .expect_stmt("select count(*) from users")
        .expect_result([(2,)])
    )
    async with mock as db:
        res = await db.execute("select * from users")
        assert len(res) == 2

    count = await db.fetch_val("select count(*) from users")
    assert count == 2
