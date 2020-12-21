import os

from flask import current_app, g
from db.repositories.factories import (
    make_files_sql_repo,
    make_files_mongo_repo,
    get_sql_db,
)
from db.repositories import IFilesRepository


def get_db() -> IFilesRepository:
    if "db" not in g:
        g.db = (
            make_files_mongo_repo()
            if not current_app.testing
            else make_files_sql_repo()
        )

    return g.db


def close_db(e=None):
    g.pop("db", None)
    db = get_sql_db()

    if db is not None:
        db.close()


def init_db():
    db = get_sql_db()

    schema_file = os.path.join(os.path.dirname(__file__), "schema.sql")

    with open(schema_file, "rb") as f:
        db.executescript(f.read().decode("utf8"))
