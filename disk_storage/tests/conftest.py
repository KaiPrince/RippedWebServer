import os
import pytest
from web_server import create_app
from storage.utils import copyfile


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