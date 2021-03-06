import os
import sys
from io import BytesIO

import pytest


class TestStorage:
    # @pytest.mark.parametrize([])
    def test_index(self, client, auth_token):
        """ Index page displays a file name. """
        # Arrange
        # Act
        response = client.get("/storage/", headers={"Authorization": auth_token})

        # Assert
        assert response.status_code == 200
        assert b"test.txt" in response.data

    @pytest.mark.parametrize("chunk", [True, False])
    def test_upload(self, client, app, auth_token, chunk):
        """ File can be uploaded to web server. """

        # Arrange
        file_path = "test2.txt"
        contents = b"my file contents"
        content_size = sys.getsizeof(contents) - 1

        content_range = f"0-{content_size}"
        content_total = content_size

        # Act

        response = client.post(
            "/storage/create",
            headers={"Authorization": auth_token},
            json={
                "file_path": file_path,
                "content_total": str(content_size),
            },
        )
        assert response.status_code in [200, 201]
        assert file_path in response.json["file_path"]
        assert response.json["upload_url"] == "/storage/create/" + file_path

        with app.app_context():
            assert file_path in os.listdir(app.config["UPLOAD_FOLDER"])

        # ..splitting string into equal halves
        contents_parts = (
            contents[: len(contents) // 2],
            contents[len(contents) // 2 :] if chunk else contents,
        )

        for index, part in enumerate(contents_parts):
            begin = sys.getsizeof(part) * index
            end = begin + sys.getsizeof(part)

            content_range = f"{begin}-{end}"
            content_total = sys.getsizeof(contents)

            response = client.put(
                "/storage/create/" + file_path,
                buffered=True,
                headers={
                    "Authorization": auth_token,
                    "Content-Range": f"bytes {content_range}/{content_total}",
                    # "file_path": file_path,
                },
                data=BytesIO(part),
            )
            assert response.status_code == 200

        # Assert

        with app.app_context():
            assert file_path in os.listdir(app.config["UPLOAD_FOLDER"])
            with open(os.path.join(app.config["UPLOAD_FOLDER"], file_path), "rb") as f:
                assert contents in f.read()

    def test_download_file(self, client, app, auth_token):
        """ Existing file can be downloaded. """

        # Arrange
        file_path = "test.txt"

        # Act
        response = client.get(
            f"/storage/download/{file_path}", headers={"Authorization": auth_token}
        )

        # Assert
        assert response.status_code == 200
        assert b"test content" in response.data

    def test_delete_file(self, client, app, auth_token):
        """ Existing file can be deleted. """
        # Arrange
        file_path = "test.txt"

        # Act
        response = client.post(
            "/storage/delete/" + file_path,
            headers={
                "Authorization": auth_token,
                # "file_path": file_path,
            },
        )

        # Assert
        assert response.status_code in [200, 302]
        with app.app_context():
            assert file_path not in os.listdir(app.config["UPLOAD_FOLDER"])
