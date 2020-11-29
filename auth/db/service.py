import os
import sqlite3
from sqlite3 import Connection

from flask import current_app, g
from werkzeug.security import generate_password_hash

from .config import DEFAULT_PASSWORD, DEFAULT_USER


def get_db() -> Connection:
    if "db" not in g:
        # client = pymongo.MongoClient("mongodb+srv://dbAdmin:<password>@cluster0.o29to.mongodb.net/<dbname>?retryWrites=true&w=majority")
        # db = client.test

        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    schema_file = os.path.join(os.path.dirname(__file__), "schema.sql")

    with open(schema_file, "rb") as f:
        db.executescript(f.read().decode("utf8"))

    create_user(DEFAULT_USER, DEFAULT_PASSWORD)
    create_permissions()


def create_user(username, password):
    db = get_db()

    db.execute(
        "INSERT INTO user (username, password) VALUES (?, ?)",
        (username, generate_password_hash(password)),
    )
    db.commit()


def create_permissions():
    db = get_db()

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

    user_permissions = [(1, 1), (1, 2), (1, 3), (1, 4)]

    for x in user_permissions:
        db.execute(
            "INSERT INTO user_permissions (user_id, permission_id) " "VALUES (?, ?)",
            [x[0], x[1]],
        )
        db.commit()
