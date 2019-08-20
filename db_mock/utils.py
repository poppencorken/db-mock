import sqlalchemy
import sqlparse


def _unpack_params(stmt, params):
    return params


def _normalize(stmt, dialect):
    if isinstance(stmt, sqlalchemy.sql.Selectable):
        query = str(stmt.compile(dialect=dialect))
    else:
        query = stmt

    return sqlparse.format(
        query,
        reindent=True,
        keyword_case="upper",
        use_space_around_operators=True,
    ).rstrip(";")
