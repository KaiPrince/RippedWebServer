import sys
from datetime import datetime
from io import BytesIO
from unittest.mock import MagicMock

from flask import Flask

# import pytest
from db.service import get_db
from werkzeug.datastructures import FileStorage


class TestFiles:
    def test_index(self, client, auth_token):
        """ Index page displays a file name. """
        # Arrange
        # Act
        response = client.get(
            "/files/",
            headers={
                "Authorization": auth_token,
            },
        )

        # Assert
        assert response.status_code == 200
        assert b"test.txt" in response.data

    def test_upload(
        self,
        client,
        app: Flask,
        auth_token,
        mock_files_repo: MagicMock,
        mocker: MagicMock,
        disk_storage_service_url,
    ):
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

        _get_response = mocker.MagicMock()
        _get_response.json.return_value = {"file_size": str(content_size)}

        mock_files_repo.put.return_value = _get_response

        data = BytesIO(contents)

        json = {
            "file_name": filename,
            "user_id": user_id,
            "file_path": file_path,
            "content_total": str(content_size),
        }

        # Act
        response = client.post(
            "/files/create",
            headers={
                "Authorization": auth_token,
            },
            json=json,
        )

        assert response.status_code < 400  # No error

        response = client.put(
            "/files/create",
            buffered=True,
            headers={
                "Authorization": auth_token,
                "Content-Range": f"bytes {content_range}/{content_total}",
                "file_id": str(file_id),
            },
            data=data,
        )

        # Assert
        assert response.status_code < 400  # No error

        # ..repo is called

        mock_files_repo.post.assert_called_once_with(
            disk_storage_service_url + "/storage/create",
            json={
                "file_path": file_path,
                "content_total": str(content_size),
            },
        )

        # ..temporariliy override the equality comparator
        FileStorage.__eq__ = lambda self, obj: self.filename == obj.filename

        mock_files_repo.put.assert_called_once_with(
            disk_storage_service_url + "/storage/create",
            headers={
                "Content-Range": f"bytes 0-{content_size}/{content_size}",
                "file_path": file_path,
            },
            data=contents,
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
        self,
        client,
        app: Flask,
        auth_token,
        mock_files_repo: MagicMock,
        mocker: MagicMock,
        disk_storage_service_url,
    ):
        """ File can be uploaded to web server. """

        # Arrange
        filename = "test2.txt"
        contents = b"my file contents"
        content_size = sys.getsizeof(contents) - 1
        file_path = filename

        user_id = 1
        file_id = 2

        _get_response = mocker.MagicMock()
        _get_response.json.return_value = {"file_size": str(content_size)}

        mock_files_repo.put.return_value = _get_response

        json = {
            "file_name": filename,
            "user_id": user_id,
            "file_path": file_path,
            "content_total": str(content_size),
        }

        # Act
        response = client.post(
            "/files/create",
            headers={
                "Authorization": auth_token,
            },
            json=json,
        )

        # Assert

        assert response.status_code < 400  # No error

        mock_files_repo.post.assert_called_once_with(
            disk_storage_service_url + "/storage/create",
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

            data = BytesIO(part)

            # Act
            response = client.put(
                "/files/create",
                buffered=True,
                headers={
                    "Authorization": auth_token,
                    "Content-Range": f"bytes {content_range}/{content_total}",
                    "file_id": str(file_id),
                },
                data=data,
            )

            # Assert
            assert response.status_code < 400  # No error

            mock_files_repo.put.assert_called_with(
                disk_storage_service_url + "/storage/create",
                headers={
                    "Content-Range": f"bytes {content_range}/{content_total}",
                    "file_path": file_path,
                },
                data=part,
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
        self,
        app: Flask,
        client,
        auth_token,
        mock_files_repo: MagicMock,
        mocker: MagicMock,
        disk_storage_service_url,
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
        response = client.get(
            "/files/1",
            headers={
                "Authorization": auth_token,
            },
        )

        # Assert
        assert response.json == {
            "id": file_id,
            "user_id": 1,
            "name": filename,
            "file_path": file_path,
            "uploaded": file_uploaded.strftime("%a, %d %b %Y %H:%M:%S GMT"),
        }
        assert response.status_code == 200

        response = client.get(
            "/files/content/1",
            headers={
                "Authorization": auth_token,
            },
        )
        assert response.status_code == 200
        assert response.data == bytes(content, "utf-8")

        mock_files_repo.get.assert_called_with(
            disk_storage_service_url + "/storage/file-content",
            headers={
                "file_path": file_path,
            },
        )

    def test_delete_file(
        self,
        client,
        app: Flask,
        auth_token,
        mock_files_repo: MagicMock,
        disk_storage_service_url,
    ):
        """ Existing file can be deleted. """
        # Arrange
        file_id = 1
        file_path = "test.txt"

        # Act
        response = client.post(
            "/files/delete/" + str(file_id),
            headers={
                "Authorization": auth_token,
            },
        )

        # Assert
        assert response.status_code in [200, 302]
        with app.app_context():
            db = get_db()
            count = db.execute(
                "SELECT COUNT(id) FROM user_file WHERE id = ?", str(file_id)
            ).fetchone()[0]
            assert count == 0

        mock_files_repo.post.assert_called_with(
            disk_storage_service_url + "/storage/delete",
            headers={
                "file_path": file_path,
            },
        )
