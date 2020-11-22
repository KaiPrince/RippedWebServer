# import pytest

from io import BytesIO
import sys
from unittest.mock import MagicMock
from werkzeug.datastructures import FileStorage


class TestFiles:
    def test_index(self, client, mock_files_repo: MagicMock, mocker: MagicMock):
        """ Index page displays a file name. """
        # Arrange

        _get_response = mocker.MagicMock()
        _get_response.json.return_value = {
            "files": [{"id": 1, "file_name": "test.txt"}]
        }

        mock_files_repo.get.return_value = _get_response
        # Act
        response = client.get("/files/")

        # Assert
        assert response.status_code == 200
        assert b"test.txt" in response.data

        mock_files_repo.get.assert_called_once_with("http://localhost:5003" + "/")

    def test_upload(
        self, client, auth, app, mock_files_repo: MagicMock, mocker: MagicMock
    ):
        """ File can be uploaded to web server. """
        # Arrange
        auth.login()
        assert client.get("/files/create").status_code == 200

        filename = "test2.txt"
        contents = b"my file contents"

        data = {
            "file_name": filename,
            "file": (
                BytesIO(contents),
                filename,
            ),
        }

        # Act
        response = client.post(
            "/files/create",
            buffered=True,
            content_type="multipart/form-data",
            data=data,
        )

        # Assert
        assert response.status_code < 400  # No error

        # ..repo is called
        content_size = sys.getsizeof(contents) - 1

        mock_files_repo.post.assert_called_once_with(
            "http://localhost:5003" + "/files/create",
            json={
                "file_name": filename,
                "user_id": 2,
                "file_path": filename,
                "content_total": str(content_size),
            },
        )

        # ..temporariliy override the equality comparator
        FileStorage.__eq__ = lambda self, obj: self.filename == obj.filename

        mock_files_repo.put.assert_called_once_with(
            "http://localhost:5003" + "/files/create",
            headers={
                "Content-Range": f"bytes 0-{content_size}/{content_size}",
                "file_id": str(1),
            },
            data=FileStorage(
                BytesIO(contents), filename=filename, content_type="text/plain"
            ),
        )

    def test_upload_parts(self, client, auth, app, mock_files_repo: MagicMock):
        """ File can be uploaded to web server. """

        # Arrange
        auth.login()
        assert client.get("/files/create").status_code == 200

        filename = "test2.txt"
        contents = b"my file contents"

        # ..splitting string into equal halves
        contents_parts = contents[: len(contents) // 2], contents[len(contents) // 2 :]

        for index, part in enumerate(contents_parts):
            begin = sys.getsizeof(part) * index
            end = begin + sys.getsizeof(part)

            content_range = f"{begin}-{end}"
            content_total = sys.getsizeof(contents)

            data = {
                "file_name": filename,
                "file": (
                    BytesIO(part),
                    filename,
                ),
            }

            # Act
            response = client.post(
                "/files/create",
                buffered=True,
                headers={"Content-Range": f"bytes {content_range}/{content_total}"},
                content_type="multipart/form-data",
                data=data,
            )

            # Assert
            assert response.status_code < 400  # No error

            # ..temporariliy override the equality comparator
            FileStorage.__eq__ = lambda self, obj: self.filename == obj.filename

            mock_files_repo.put.assert_called_with(
                "http://localhost:5003" + "/files/create",
                headers={
                    "Content-Range": f"bytes {content_range}/{content_total}",
                    "file_id": str(1),
                },
                data=FileStorage(
                    BytesIO(contents), filename=filename, content_type="text/plain"
                ),
            )

        mock_files_repo.post.assert_called_once_with(
            "http://localhost:5003" + "/files/create",
            json={
                "file_name": filename,
                "user_id": 2,
                "file_path": filename,
                "content_total": str(content_total),
            },
        )

    def test_read_file(self, client, auth):
        """ Existing file can be read. """
        # Arrange
        auth.login()

        # Act
        response = client.get("/files/detail/1")

        # Assert
        assert response.status_code == 200
        assert b"test.txt" in response.data
        assert b"test content" in response.data

    def test_delete_file(self, client, app, auth):
        """ Existing file can be deleted. """
        # Arrange
        auth.login()

        # Act
        response = client.post("/files/delete/1")

        # Assert
        assert response.status_code in [200, 302]
