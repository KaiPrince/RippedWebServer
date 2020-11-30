import os

import pytest
from storage.utils import copyfile
from web_server import create_app

UPLOAD_FOLDER = os.path.join(".", "tests", "uploads")


@pytest.fixture
def app(tmp_path):

    temp_uploads_folder = tmp_path
    # Copy files in test uploads folder to temp directory
    filesToCopy = os.listdir(UPLOAD_FOLDER)
    for f in filesToCopy:
        with open(os.path.join(UPLOAD_FOLDER, f), "rb") as src:
            dest_file = temp_uploads_folder / f
            copyfile(src, dest_file)

    app_config = {"UPLOAD_FOLDER": temp_uploads_folder}
    app = create_app(app_config)

    # Setup
    with app.app_context():
        pass

    # Provide resource
    yield app

    # Teardown
    pass


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def auth_token() -> str:
    """
    {
        "sub": "1",
        "name": "admin",
        "permissions": ["read: disk_storage", "write: disk_storage"],
        "iat": 1516239022
    }
    """
    return (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
        "eyJzdWIiOiIxIiwibmFtZSI6ImFkbWluIiwicGVybWlzc"
        "2lvbnMiOlsicmVhZDogZGlza19zdG9yYWdlIiwid3JpdGU6"
        "IGRpc2tfc3RvcmFnZSJdLCJpYXQiOjE1MTYyMzkwMjJ9."
        "4bNBGPPgRThOmkJcf_AUCI-RGCejUsDPUzjoJtX92Pc"
    )
