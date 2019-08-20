dbmock
=======

This is *dbmock*, the convenient DB-API 2.0 and async database mocking
library. With *dbmock* you can test your database layer code without having to
have a database running for your tests. Have a look at the following example:

.. code:: python


    # First we have a function
    def get_book_by_author_name(db, name):
        autor_id = db.execute(
            "SELECT id FROM users where name = :name;",
            {'name': name}).fetchval()
        return db.execute(
            "select title from books where author_id = :id limit 1",
            {'id': author_id}
        ).fetchval()

    # Then we define our expectations to the function. Asynchronous database
    # drivers are also supported by the `DBMockAsync` and `DBMockDatabases`
    # classes.
    from db_mock import DBMockSync
    mock = (
        DBMockSync()
        .expect_stmt("select id from users where name = :name",
                     {'name': 'Douglas Adams'})
        .expect_result([(42,)])
        .expect_stmt("select title from books where author_id = :id limit 1",
                     {'id': 42})
        .expect_result([('The Hitchhikers Guide To The Galaxy',)])
    )

    # Then we run the function. If not all SQL queries are executed in the
    # expected order, an exception will be raised.
    with mock as db:
        title = get_book_by_author_name(db, 'Douglas Adams')
        assert title == u'The Hitchikers Guide To The Galaxy'


-----

.. contents:: **Table of Contents**
    :backlinks: none

Installation
------------

db-mock is distributed on `PyPI <https://pypi.org>`_ as a universal
wheel and is available on Linux/macOS (and possibly Windows) and supports
Python 2.7/3.5+ and PyPy/PyPy3.

.. code-block:: bash

    $ pip install db-mock

License
-------

db-mock is distributed under the terms of both

- `MIT License <https://choosealicense.com/licenses/mit>`_
- `Apache License, Version 2.0 <https://choosealicense.com/licenses/apache-2.0>`_

at your option.
