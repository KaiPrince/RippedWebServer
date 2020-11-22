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

    def test_upload_parts(self, client, auth, app):
        """ File can be uploaded to web server. """
        # Arrange
        auth.login()
        assert client.get("/files/create").status_code == 200

        filename = "test2.txt"
        contents = b"my file contents"

        # Splitting string into equal halves
        contents_parts = contents[: len(contents) // 2], contents[len(contents) // 2 :]

        for index, part in enumerate(contents_parts):
            content_range = f"{len(part) * index}-{len(part)}"
            content_total = len(contents)

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
