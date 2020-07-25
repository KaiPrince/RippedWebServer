import os
import tempfile

import pytest
from web_server import create_app
from web_server.db import get_db, init_db
from web_server.utils import copyfile

with open(os.path.join(os.path.dirname(__file__), "data.sql"), "rb") as f:
    _data_sql = f.read().decode("utf8")

UPLOAD_FOLDER = os.path.join(".", "tests", "uploads")


@pytest.fixture
def app(tmp_path):
    db_fd, db_path = tempfile.mkstemp()

    temp_uploads_folder = tmp_path
    # Copy files in test uploads folder to temp directory
    filesToCopy = os.listdir(UPLOAD_FOLDER)
    for f in filesToCopy:
        with open(os.path.join(UPLOAD_FOLDER, f), "rb") as src:
            dest_file = temp_uploads_folder / f
            copyfile(src, dest_file)

    app = create_app(
        {"TESTING": True, "DATABASE": db_path, "UPLOAD_FOLDER": temp_uploads_folder,}
    )

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)

    # Remove files in temp directory
    # filesToRemove = [os.path.join(UPLOAD_FOLDER, f) for f in os.listdir(UPLOAD_FOLDER)]
    # for f in filesToRemove:
    #     os.remove(f)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
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
