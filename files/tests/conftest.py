import os
import tempfile

import pytest
from pytest_mock import MockerFixture
from unittest.mock import MagicMock
from files import create_app
from db.service import get_db, init_db
from files.utils import copyfile

with open(os.path.join(os.path.dirname(__file__), "data.sql"), "rb") as f:
    _data_sql = f.read().decode("utf8")

UPLOAD_FOLDER = os.path.join(".", "tests", "uploads")


@pytest.fixture
def app(tmp_path, mock_files_repo):
    db_fd, db_path = tempfile.mkstemp()

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
            "DATABASE": db_path,
            "UPLOAD_FOLDER": temp_uploads_folder,
        }
    )

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def mock_files_repo(mocker: MockerFixture) -> MagicMock:
    mock_func = mocker.patch("files.repository.requests")

    return mock_func
