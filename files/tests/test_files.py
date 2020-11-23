import pytest
import os

from io import BytesIO
from db.service import get_db
import sys
from unittest.mock import MagicMock
from werkzeug.datastructures import FileStorage
from datetime import datetime


class TestFiles:
    def test_index(self, client):
        """ Index page displays a file name. """
        # Arrange
        # Act
        response = client.get("/files/")

        # Assert
        assert response.status_code == 200
        assert b"test.txt" in response.data

    def test_upload(self, client, app, mock_files_repo: MagicMock, mocker: MagicMock):
        """ File can be uploaded to web server. """
        # Arrange
        filename = "test2.txt"
        contents = b"my file contents"
        content_size = sys.getsizeof(contents) - 1
        file_path = filename
        user_id = 2
        file_id = 2

        content_range = f"0-{content_size}"
        content_total = content_size

        data = {
            "file_name": filename,
            "file": (
                BytesIO(contents),
                filename,
            ),
        }

        json = {
            "file_name": filename,
            "user_id": user_id,
            "file_path": file_path,
            "content_total": str(content_size),
        }

        # Act
        response = client.post("/files/create", json=json)

        assert response.status_code < 400  # No error

        response = client.put(
            "/files/create",
            buffered=True,
            content_type="multipart/form-data",
            headers={
                "Content-Range": f"bytes {content_range}/{content_total}",
                "file_id": str(file_id),
            },
            data=data,
        )

        # Assert
        assert response.status_code < 400  # No error

        # ..repo is called

        mock_files_repo.post.assert_called_once_with(
            "http://localhost:5002" + "/storage/create",
            json={
                "file_path": file_path,
                "content_total": str(content_size),
            },
        )

        # ..temporariliy override the equality comparator
        FileStorage.__eq__ = lambda self, obj: self.filename == obj.filename

        mock_files_repo.put.assert_called_once_with(
            "http://localhost:5002" + "/storage/create",
            headers={
                "Content-Range": f"bytes 0-{content_size}/{content_size}",
                "file_path": file_path,
            },
            data=FileStorage(
                BytesIO(contents), filename=filename, content_type="text/plain"
            ),
        )

        with app.app_context():
            db = get_db()

            count = db.execute("SELECT COUNT(id) FROM user_file").fetchone()[0]
            assert count == 2

            db_file = db.execute(
                "SELECT f.id, file_name as name, uploaded, user_id, file_path"
                " FROM user_file f"
                " WHERE f.id = ?"
                " ORDER BY uploaded DESC",
                str(file_id),
            ).fetchone()
            assert db_file["name"] == filename
            assert db_file["user_id"] == user_id
            assert db_file["file_path"] == file_path

    def test_upload_parts(
        self, client, app, mock_files_repo: MagicMock, mocker: MagicMock
    ):
        """ File can be uploaded to web server. """

        # Arrange
        filename = "test2.txt"
        contents = b"my file contents"
        content_size = sys.getsizeof(contents) - 1
        file_path = filename

        user_id = 1
        file_id = 2

        json = {
            "file_name": filename,
            "user_id": user_id,
            "file_path": file_path,
            "content_total": str(content_size),
        }

        # Act
        response = client.post("/files/create", json=json)

        # Assert

        assert response.status_code < 400  # No error

        mock_files_repo.post.assert_called_once_with(
            "http://localhost:5002" + "/storage/create",
            json={
                "file_path": file_path,
                "content_total": str(content_size),
            },
        )

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
            response = client.put(
                "/files/create",
                buffered=True,
                headers={
                    "Content-Range": f"bytes {content_range}/{content_total}",
                    "file_id": str(file_id),
                },
                content_type="multipart/form-data",
                data=data,
            )

            # Assert
            assert response.status_code < 400  # No error

            # ..temporariliy override the equality comparator
            FileStorage.__eq__ = lambda self, obj: self.filename == obj.filename

            mock_files_repo.put.assert_called_with(
                "http://localhost:5002" + "/storage/create",
                headers={
                    "Content-Range": f"bytes {content_range}/{content_total}",
                    "file_path": file_path,
                },
                data=FileStorage(
                    BytesIO(contents), filename=filename, content_type="text/plain"
                ),
            )

        with app.app_context():
            db = get_db()

            count = db.execute("SELECT COUNT(id) FROM user_file").fetchone()[0]
            assert count == 2

            db_file = db.execute(
                "SELECT f.id, file_name as name, uploaded, user_id, file_path"
                " FROM user_file f"
                " WHERE f.id = ?"
                " ORDER BY uploaded DESC",
                str(file_id),
            ).fetchone()
            assert db_file["name"] == filename
            assert db_file["user_id"] == user_id
            assert db_file["file_path"] == file_path

    def test_read_file(
        self, app, client, mock_files_repo: MagicMock, mocker: MagicMock
    ):
        """ Existing file can be read. """
        # Arrange
        file_id = 1
        filename = "test.txt"
        file_path = "test.txt"
        content = "test content"

        with app.app_context():
            db = get_db()
            file_uploaded: datetime = db.execute(
                "SELECT uploaded"
                " FROM user_file f"
                " WHERE f.id = ?"
                " ORDER BY uploaded DESC",
                str(file_id),
            ).fetchone()[0]

        _get_response = mocker.MagicMock()
        _get_response.content = content

        mock_files_repo.get.return_value = _get_response

        # Act
        response = client.get("/files/1")

        # Assert
        assert response.json == {
            "id": file_id,
            "user_id": 1,
            "name": filename,
            "file_path": file_path,
            "uploaded": file_uploaded.strftime("%a, %d %b %Y %H:%M:%S GMT"),
        }
        assert response.status_code == 200

        response = client.get("/files/content/1")
        assert response.status_code == 200
        assert response.data == bytes(content, "utf-8")

        mock_files_repo.get.assert_called_with(
            "http://localhost:5002" + "/storage/file-content",
            headers={
                "file_path": file_path,
            },
        )

    def test_delete_file(self, client, app, mock_files_repo):
        """ Existing file can be deleted. """
        # Arrange
        file_id = 1
        file_path = "test.txt"

        # Act
        response = client.post("/files/delete/" + str(file_id))

        # Assert
        assert response.status_code in [200, 302]
        with app.app_context():
            db = get_db()
            count = db.execute(
                "SELECT COUNT(id) FROM user_file WHERE id = ?", str(file_id)
            ).fetchone()[0]
            assert count == 0

        mock_files_repo.post.assert_called_with(
            "http://localhost:5002" + "/storage/delete",
            headers={
                "file_path": file_path,
            },
        )
