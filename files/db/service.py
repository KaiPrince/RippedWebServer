import sqlite3
import os

from flask import current_app, g


def get_db():
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
