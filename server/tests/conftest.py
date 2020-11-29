import os
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture
from web_server import create_app

from files.utils import copyfile
from flask import Flask
from authlib.jose import jwt


UPLOAD_FOLDER = os.path.join(".", "tests", "uploads")


@pytest.fixture
def app(tmp_path, mock_files_repo) -> Flask:

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
    def __init__(self, app, client, mock_func, mocker):
        self._app = app
        self._client = client
        self._mock_func = mock_func
        self._mocker = mocker

    def login(self, username="test", password="test", permissions=""):

        mock_token = jwt.encode(
            {"alg": "HS256"},
            {"sub": 2, "name": username, "permissions": permissions},
            self._app.secret_key,
        ).decode("utf-8")

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
def auth(app, client, mock_auth_repo, mocker):
    return AuthActions(app, client, mock_auth_repo, mocker)


@pytest.fixture
def mock_files_repo(mocker: MockerFixture) -> MagicMock:
    mock_func = mocker.patch("files.repository.requests")

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
