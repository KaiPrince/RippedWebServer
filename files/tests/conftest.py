import os
import tempfile
from unittest.mock import MagicMock

import pytest
import requests
from authlib.jose import jwt
from flask import Flask
from pytest_mock import MockerFixture

from db.repositories.factories import get_sql_db
from db.service import init_db
from files import create_app

with open(os.path.join(os.path.dirname(__file__), "data.sql"), "rb") as f:
    _data_sql = f.read().decode("utf8")


@pytest.fixture
def app(mock_disk_repo) -> Flask:
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
def client(app: Flask):
    return app.test_client()


@pytest.fixture
def runner(app: Flask):
    return app.test_cli_runner()


@pytest.fixture
def mock_disk_repo(mocker: MockerFixture) -> MagicMock:
    mock_func = mocker.patch("service_api.disk_storage.requests")

    return mock_func


@pytest.fixture
def disk_storage_service_url(app: Flask) -> str:
    return app.config["DISK_STORAGE_SERVICE_URL"]


@pytest.fixture
def public_disk_storage_service_url(app: Flask) -> str:
    return app.config["PUBLIC_DISK_STORAGE_SERVICE_URL"]


@pytest.fixture
def disk_auth_token(mocker: MockerFixture) -> str:
    token = "testauthtoken"
    mock_func = mocker.patch("files.service.create_auth_token")
    mock_func.return_value = token

    yield token

    mock_func.clear()


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
def make_request() -> requests.PreparedRequest:
    """ Consumes any arguments and returns a prepared request. """

    def func(*args, **kwargs):

        req: requests.PreparedRequest = requests.Request(
            "GET", *args, **kwargs
        ).prepare()

        return req

    return func
