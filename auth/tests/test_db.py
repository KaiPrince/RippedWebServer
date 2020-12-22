import pytest
import sqlite3
import db.command
from db.service import get_db


def test_get_close_db(app):
    with app.app_context():
        db = get_db().db
        assert db is get_db().db

    # Out of app context, db should be closed.
    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute("SELECT 1")

    assert "closed" in str(e.value)


def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr(db.command, "init_db", fake_init_db)
    result = runner.invoke(args=["init-db"])
    assert "Initialized" in result.output
    assert Recorder.called


def test_create_super_user_command(runner, app):
    with app.app_context():
        result = runner.invoke(args=["create-superuser", "admin"], input="test\ntest\n")
        assert "Created" in result.output

        db = get_db()

        assert len(db.search(lambda x: x["username"] == "admin")) == 1

        user = db.search(lambda x: x["username"] == "admin")[0]
        assert user["permissions"] == [
            {"access_level": "read", "scope": "files"},
            {"access_level": "write", "scope": "files"},
            {"access_level": "read", "scope": "disk_storage"},
            {"access_level": "write", "scope": "disk_storage"},
        ]

    del db
