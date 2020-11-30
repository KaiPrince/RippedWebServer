import sys
from datetime import datetime
from io import BytesIO
from unittest.mock import MagicMock

from flask import Flask

# import pytest
from db.service import get_db
from werkzeug.datastructures import FileStorage


class TestFiles:
    def test_index(self, client, auth_token, disk_storage_service_url):
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
        upload_url = disk_storage_service_url + "/storage/create/" + "test.txt"
        download_url = disk_storage_service_url + "/storage/download/" + "test.txt"

        assert response.status_code == 200
        assert b"test.txt" in response.data

        files = response.json["files"]
        file = files[0]
        assert file["id"] == 1
        assert file["file_name"] == "test.txt"
        assert file["file_path"] == "test.txt"
        assert file["download_url"] == download_url
        assert file["upload_url"] == upload_url

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

        upload_url = disk_storage_service_url + "/storage/create/" + file_path

        _get_response = mocker.MagicMock()
        _get_response.json.return_value = {"upload_url": upload_url}

        mock_files_repo.post.return_value = _get_response

        json = {
            "file_name": filename,
            "user_id": user_id,
            "file_path": file_path,
            "content_total": str(content_size),
        }

        # Act
        # ..create file
        response = client.post(
            "/files/create",
            headers={
                "Authorization": auth_token,
            },
            json=json,
        )

        # Assert

        # ..repo is called
        mock_files_repo.post.assert_called_once_with(
            disk_storage_service_url + "/storage/create",
            json={
                "file_path": file_path,
                "content_total": str(content_size),
            },
        )

        # ..No error
        assert response.status_code < 400
        # ..Upload url returned
        assert response.json["upload_url"] == upload_url

        # ..DB entry created
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

        with app.app_context():
            db = get_db()
            file_uploaded: datetime = db.execute(
                "SELECT uploaded"
                " FROM user_file f"
                " WHERE f.id = ?"
                " ORDER BY uploaded DESC",
                str(file_id),
            ).fetchone()[0]

        download_url = disk_storage_service_url + "/storage/download/" + file_path

        _get_response = mocker.MagicMock()
        _get_response.json.return_value = {"download_url": download_url}

        mock_files_repo.get.return_value = _get_response

        # Act
        # ..get file details
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

        # Act
        # .. get file content
        response = client.get(
            "/files/download/1",
            headers={
                "Authorization": auth_token,
            },
        )

        # Assert
        assert response.status_code == 200
        assert response.json["download_url"] == download_url

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
