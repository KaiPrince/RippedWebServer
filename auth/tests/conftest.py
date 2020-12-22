import os
import tempfile

import pytest
from authlib.jose import jwt
from flask import Flask
from flask.testing import FlaskClient

from db.repositories.factories import get_sql_db
from db.service import get_db
from db.service import init_db
from main import create_app

with open(os.path.join(os.path.dirname(__file__), "data.sql"), "rb") as f:
    _data_sql = f.read().decode("utf8")


@pytest.fixture
def app(tmp_path) -> Flask:
    db_fd, db_path = tempfile.mkstemp()

    app = create_app(
        {
            "TESTING": True,
            "DATABASE": db_path,
        }
    )

    with app.app_context():
        init_db()
        get_sql_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()


@pytest.fixture
def runner(app: Flask):
    return app.test_cli_runner()



class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username="test", password="test"):
        return self._client.post(
            "/auth/login", data={"username": username, "password": password}
        )

    def logout(self):
        return self._client.get("/auth/logout")


@pytest.fixture
def auth(client):
    return AuthActions(client)


@pytest.fixture
def auth_token(app) -> str:
    """
    {
        "sub": "1",
        "name": "test",
        "permissions": ["read: files", "write: files"],
        "iat": 1516239022
    }
    """

    username = "test"
    permissions = [
        "read: files",
        "write: files",
        "read: disk_storage",
        "write: disk_storage",
    ]

    token = jwt.encode(
        {"alg": "HS256"},
        {"sub": 2, "name": username, "permissions": permissions},
        app.config["JWT_KEY"],
    ).decode("utf-8")

    return token


@pytest.fixture
def make_auth_token(app, make_token):
    def make_payload(user_id, username, permissions):
        return {"sub": user_id, "name": username, "permissions": permissions}

    def make(user_id, username, permissions=[]):
        payload = make_payload(user_id, username, permissions)
        token = make_token(payload)

        return token

    return make


@pytest.fixture
def make_token(app):
    """ Sign a JWT. """

    def sign(payload):

        token = jwt.encode(
            {"alg": "HS256"},
            payload,
            app.config["JWT_KEY"],
        ).decode("utf-8")

        return token

    return sign
