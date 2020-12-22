import os
from sqlite3 import Connection

from flask import current_app, g
from werkzeug.security import generate_password_hash


from db.repositories import IUsersRepository
from db.repositories.factories import (
    get_sql_db,
    make_users_mongo_repo,
    make_users_sql_repo,
)


def get_db() -> IUsersRepository:
    if "db" not in g:
        g.db = (
            make_users_mongo_repo()
            if not current_app.testing
            else make_users_sql_repo()
        )

    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        # Call destructor to run cleanup
        del db


def init_db():
    """ Run initialization and seed database. """

    # Testing database only
    if current_app.testing:
        sql_db = get_sql_db()
        init_sql_schema(sql_db)


def init_sql_schema(db: Connection):
    # Run schema script
    schema_file = os.path.join(os.path.dirname(__file__), "schema.sql")

    with open(schema_file, "rb") as f:
        db.executescript(f.read().decode("utf8"))

    # Populate permissions table
    permissions = [
        ("read", "files"),
        ("write", "files"),
        ("read", "disk_storage"),
        ("write", "disk_storage"),
    ]

    for x in permissions:
        db.execute(
            "INSERT INTO permission (access_level, scope) VALUES (?, ?)", [x[0], x[1]]
        )
        db.commit()


def create_super_user(username, password):

    permissions = [
        ("read", "files"),
        ("write", "files"),
        ("read", "disk_storage"),
        ("write", "disk_storage"),
    ]

    permissions = [{"access_level": x, "scope": y} for x, y in permissions]

    return create_user(username, password, permissions)


def create_user(username, password, permissions):
    db = get_db()

    password = generate_password_hash(password)

    return db.create(username, password, permissions)
