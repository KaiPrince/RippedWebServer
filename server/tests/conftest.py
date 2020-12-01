import os
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture
from web_server import create_app

from files.utils import copyfile
from flask import Flask
from authlib.jose import jwt
import requests


UPLOAD_FOLDER = os.path.join(".", "tests", "uploads")


@pytest.fixture
def app(tmp_path, mock_files_repo, mock_disk_storage_repo) -> Flask:

    temp_uploads_folder = tmp_path
    # Copy files in test uploads folder to temp directory
    filesToCopy = os.listdir(UPLOAD_FOLDER)
    for f in filesToCopy:
        with open(os.path.join(UPLOAD_FOLDER, f), "rb") as src:
            dest_file = temp_uploads_folder / f
            copyfile(src, dest_file)

    app = create_app(
        {
            "TESTING": True,
            "UPLOAD_FOLDER": temp_uploads_folder,
        }
    )

    yield app


@pytest.fixture
def client(app: Flask):
    return app.test_client()


@pytest.fixture
def runner(app: Flask):
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client, auth_token, mock_func, mocker):
        self._auth_token = auth_token
        self._client = client
        self._mock_func = mock_func
        self._mocker = mocker

    def login(self, username="test", password="test", permissions=""):

        mock_token = self._auth_token

        _get_response = self._mocker.MagicMock()
        _get_response.json.return_value = {"JWT": mock_token}

        self._mock_func.post.return_value = _get_response

        response = self._client.post(
            "/auth/login", data={"username": username, "password": password}
        )

        self._mock_func.clear()

        return response

    def logout(self):
        return self._client.get("/auth/logout")


@pytest.fixture
def auth(client, auth_token, mock_auth_repo, mocker):
    return AuthActions(client, auth_token, mock_auth_repo, mocker)


@pytest.fixture
def mock_files_repo(mocker: MockerFixture) -> MagicMock:
    mock_func = mocker.patch("files.service_api.files.requests")

    return mock_func


@pytest.fixture
def mock_disk_storage_repo(mocker: MockerFixture) -> MagicMock:
    mock_func = mocker.patch("files.service_api.disk_storage.requests")

    return mock_func


@pytest.fixture
def files_service_url(app: Flask) -> str:
    return app.config["FILES_SERVICE_URL"]


@pytest.fixture
def mock_auth_repo(mocker: MockerFixture) -> MagicMock:
    mock_func = mocker.patch("auth.service.requests")

    return mock_func


@pytest.fixture
def auth_service_url(app: Flask) -> str:
    return app.config["AUTH_SERVICE_URL"]


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
