dbmock
=======

This is *dbmock*, the convenient DB-API 2.0 and async database mocking
library. With *dbmock* you can test your database layer code without having to
have a database running for your tests. Have a look at the following example:

.. code:: python

    from db_mock import DBMockSync
    mock = (
        DBMockSync()
        .expect_stmt("select email from users where id = 42")
        .expect_result([(u'douglas@example.com',)])
        .expect_stmt(
            "insert into users (id, email) VALUES (:id, :email)",
            {'id': 17, 'email': u'iain@example.com'},
        )
        .expect_lastrowid(100)
    )
    def do_stuff_with_users(db):
        db.execute("SELECT email    FROM   users where id=42;")
        # Just for demonstration purposes...
        assert result.fetchval() == u'douglas@example.com'
        ins = db.execute(
            "INSERT into users (id,email) values (:id,:email)",
            {'id': 17, 'email': u'iain@example.com'},
        )
        return ins.lastrowid

    with mock as db:
        lastrowid = do_stuff_with_users(db)
        assert lastrowid == 100


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
