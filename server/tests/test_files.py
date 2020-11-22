# import pytest

from io import BytesIO


class TestFiles:
    def test_index(self, client):
        """ Index page displays a file name. """
        # Arrange
        # Act
        response = client.get("/files/")

        # Assert
        assert response.status_code == 200
        assert b"test.txt" in response.data

    def test_upload(self, client, auth, app):
        """ File can be uploaded to web server. """
        # Arrange
        auth.login()
        assert client.get("/files/create").status_code == 200

        data = {
            "file_name": "test2.txt",
            "file": (
                BytesIO(b"my file contents"),
                "test2.txt",
            ),
        }

        # Act

        response_2 = client.post(
            "/files/create",
            buffered=True,
            content_type="multipart/form-data",
            data=data,
        )

        # Assert
        assert response_2.status_code < 400  # No error

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
