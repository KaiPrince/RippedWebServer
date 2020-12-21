import os

from flask import current_app, g
from db.repositories.factories import get_sql_db


def get_db():
    if "db" not in g:
        g.db = get_sql_db()

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
