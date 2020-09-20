import pytest
import os

from io import BytesIO


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
        data = {
            "file_name": file_name,
            "file": (
                BytesIO(b"my file contents"),
                file_name,
            ),
        }

        # Act

        client.post(
            "/storage/create",
            buffered=True,
            content_type="multipart/form-data",
            data=data,
        )

        # Assert

        with app.app_context():
            assert file_name in os.listdir(app.config["UPLOAD_FOLDER"])

    def test_read_file(self, client):
        """ Existing file can be read. """
        # Arrange

        # Act
        response = client.post("/storage/detail", data={"file_name": "test.txt"})

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
