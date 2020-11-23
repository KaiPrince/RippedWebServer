import os
import sys
from io import BytesIO

import pytest


class TestStorage:
    # @pytest.mark.parametrize([])
    def test_index(self, client):
        """ Index page displays a file name. """
        # Arrange
        # Act
        response = client.get("/storage/")

        # Assert
        assert response.status_code == 200
        assert b"test.txt" in response.data

    def test_upload(self, client, app):
        """ File can be uploaded to web server. """

        # Arrange
        file_name = "test2.txt"
        file_path = "test2.txt"
        contents = b"my file contents"
        content_size = sys.getsizeof(contents) - 1

        content_range = f"0-{content_size}"
        content_total = content_size

        data = {
            "file_name": file_name,
            "file": (
                BytesIO(contents),
                file_name,
            ),
        }

        json = {
            "file_path": file_path,
            "content_total": str(content_size),
        }

        # Act

        response = client.post(
            "/storage/create",
            json=json,
        )
        assert response.status_code in [200, 201]
        assert file_path in response.json["file_name"]

        response = client.put(
            "/storage/create",
            buffered=True,
            content_type="multipart/form-data",
            headers={
                "Content-Range": f"bytes {content_range}/{content_total}",
                "file_path": file_path,
            },
            data=data,
        )
        assert response.status_code == 200

        # Assert

        with app.app_context():
            assert file_path in os.listdir(app.config["UPLOAD_FOLDER"])
            with open(os.path.join(app.config["UPLOAD_FOLDER"], file_path), "rb") as f:
                assert contents in f.read()

    def test_upload_parts(self, client, app):
        """ File can be uploaded to web server. """

        # Arrange
        file_name = "test2.txt"
        file_path = "test2.txt"
        contents = b"my file contents"
        content_size = sys.getsizeof(contents) - 1

        content_range = f"0-{content_size}"
        content_total = content_size

        json = {
            "file_path": file_path,
            "content_total": str(content_size),
        }

        # Act

        response = client.post(
            "/storage/create",
            json=json,
        )
        assert response.status_code in [200, 201]
        assert file_path in response.json["file_name"]

        with app.app_context():
            assert file_path in os.listdir(app.config["UPLOAD_FOLDER"])

        # ..splitting string into equal halves
        contents_parts = contents[: len(contents) // 2], contents[len(contents) // 2 :]

        for index, part in enumerate(contents_parts):
            begin = sys.getsizeof(part) * index
            end = begin + sys.getsizeof(part)

            content_range = f"{begin}-{end}"
            content_total = sys.getsizeof(contents)

            data = {
                "file_name": file_name,
                "file": (
                    BytesIO(part),
                    file_name,
                ),
            }

            response = client.put(
                "/storage/create",
                buffered=True,
                content_type="multipart/form-data",
                headers={
                    "Content-Range": f"bytes {content_range}/{content_total}",
                    "file_path": file_path,
                },
                data=data,
            )
            assert response.status_code == 200

        # Assert

        with app.app_context():
            assert file_path in os.listdir(app.config["UPLOAD_FOLDER"])
            with open(os.path.join(app.config["UPLOAD_FOLDER"], file_path), "rb") as f:
                assert contents in f.read()

    def test_read_file(self, client):
        """ Existing file can be read. """
        # Arrange
        file_path = "test.txt"

        # Act
        response = client.get(
            "/storage/file-content",
            headers={
                "file_path": file_path,
            },
        )

        # Assert
        assert response.status_code == 200
        assert b"test content" in response.data

    def test_delete_file(self, client, app):
        """ Existing file can be deleted. """
        # Arrange
        file_name = "test.txt"

        # Act
        response = client.post(f"/storage/delete/{file_name}")

        # Assert
        assert response.status_code in [200, 302]
        with app.app_context():
            assert file_name not in os.listdir(app.config["UPLOAD_FOLDER"])
