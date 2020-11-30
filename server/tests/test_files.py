# import pytest

import sys
from io import BytesIO
from unittest.mock import MagicMock

from werkzeug.datastructures import FileStorage


class TestFiles:
    def test_index(
        self,
        client,
        mock_files_repo: MagicMock,
        mocker: MagicMock,
        files_service_url,
        make_request,
    ):
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

        calls = mock_files_repo.get.call_args_list
        for call in calls:
            req = make_request(*call.args, **call.kwargs)

            assert req.url == files_service_url + "/"

    def test_upload(
        self,
        client,
        auth,
        auth_token,
        app,
        mock_files_repo: MagicMock,
        mocker: MagicMock,
        files_service_url,
        make_request,
    ):
        """ File can be uploaded to web server. """
        # Arrange
        auth.login()
        assert client.get("/files/create").status_code == 200

        # ..file data
        file_id = 1
        filename = "test2.txt"
        contents = b"my file contents"
        content_size = sys.getsizeof(contents) - 1

        # ..service data
        upload_url = "http://rippedtoastserver.ddns.net/storage/create/" + filename

        # ..mock creation response from files service
        _get_response = mocker.MagicMock()
        _get_response.json.return_value = {
            "file_id": str(file_id),
            "upload_url": upload_url,
        }
        mock_files_repo.post.return_value = _get_response

        # ..mock info response from files service
        _get_response2 = mocker.MagicMock()
        _get_response2.json.return_value = {
            "file_id": str(file_id),
            "upload_url": upload_url,
        }
        mock_files_repo.get.return_value = _get_response2

        # Act
        # ..create file
        response = client.post(
            "/files/create",
            buffered=True,
            content_type="multipart/form-data",
            data={
                "file_name": filename,
                "file": (
                    BytesIO(contents),
                    filename,
                ),
            },
        )

        # Assert
        # ..no error
        assert response.status_code < 400

        # ..files service "create" is called
        calls = mock_files_repo.post.call_args_list
        for call in calls:
            req = make_request(*call.args, **call.kwargs)

            assert req.url == files_service_url + "/files/create"
            assert req.headers == {
                "Authorization": auth_token,
                "Content-Length": "89",
                "Content-Type": "application/json",
            }
            assert call.kwargs["json"] == {
                "file_name": filename,
                "user_id": 2,
                "file_path": filename,
                "content_total": str(content_size),
            }

        # ..temporariliy override the equality comparator
        FileStorage.__eq__ = lambda self, obj: self.filename == obj.filename

        # ..disk storage service "put" is called
        calls = mock_files_repo.put.call_args_list
        for call in calls:

            kwargs = {k: v for k, v in call.kwargs.items() if k not in ["data"]}
            req = make_request(*call.args, **kwargs)

            assert req.url == upload_url
            assert req.headers == {
                "Authorization": auth_token,
                "Content-Range": f"bytes 0-{content_size}/{content_size}",
            }
            assert call.kwargs["data"] == FileStorage(
                BytesIO(contents), filename=filename, content_type="text/plain"
            )

    def test_upload_parts(
        self,
        client,
        auth,
        auth_token,
        app,
        mock_files_repo: MagicMock,
        mocker: MagicMock,
        files_service_url,
        make_request,
    ):
        """ File can be uploaded to web server. """

        # Arrange
        auth.login()
        assert client.get("/files/create").status_code == 200

        # ..file data
        file_id = 1
        filename = "test2.txt"
        contents = b"my file contents"

        # ..service data
        upload_url = "http://rippedtoastserver.ddns.net/storage/create/" + filename

        # ..mock creation response from files service
        _get_response = mocker.MagicMock()
        _get_response.json.return_value = {
            "file_id": str(file_id),
            "upload_url": upload_url,
        }
        mock_files_repo.post.return_value = _get_response

        # ..mock info response from files service
        _get_response2 = mocker.MagicMock()
        _get_response2.json.return_value = {
            "file_id": str(file_id),
            "upload_url": upload_url,
        }
        mock_files_repo.get.return_value = _get_response2

        # ..split contents into equal halves
        contents_parts = contents[: len(contents) // 2], contents[len(contents) // 2 :]

        for index, part in enumerate(contents_parts):
            begin = sys.getsizeof(part) * index
            end = begin + sys.getsizeof(part)

            content_range = f"{begin}-{end}"
            content_total = sys.getsizeof(contents)

            # Act
            # ..create file
            response = client.post(
                "/files/create",
                buffered=True,
                headers={"Content-Range": f"bytes {content_range}/{content_total}"},
                content_type="multipart/form-data",
                data={
                    "file_name": filename,
                    "file": (
                        BytesIO(part),
                        filename,
                    ),
                },
            )

            # Assert
            # ..no error
            assert response.status_code < 400

            # ..temporariliy override the equality comparator
            FileStorage.__eq__ = lambda self, obj: self.filename == obj.filename

            # ..disk storage service "put" is called
            call = mock_files_repo.put.call_args

            kwargs = {k: v for k, v in call.kwargs.items() if k not in ["data"]}
            req = make_request(*call.args, **kwargs)

            assert req.url == upload_url
            assert req.headers == {
                "Authorization": auth_token,
                "Content-Range": f"bytes {content_range}/{content_total}",
            }
            assert call.kwargs["data"] == FileStorage(
                BytesIO(contents), filename=filename, content_type="text/plain"
            )

        # ..files service "create" is called
        calls = mock_files_repo.post.call_args_list
        for call in calls:
            req = make_request(*call.args, **call.kwargs)

            assert req.url == files_service_url + "/files/create"
            assert req.headers == {
                "Authorization": auth_token,
                "Content-Length": "89",
                "Content-Type": "application/json",
            }
            assert call.kwargs["json"] == {
                "file_name": filename,
                "user_id": 2,
                "file_path": filename,
                "content_total": str(content_total),
            }

    def test_read_file(
        self,
        client,
        auth,
        auth_token,
        mock_files_repo: MagicMock,
        mocker: MagicMock,
        files_service_url,
        make_request,
    ):
        """ Existing file can be read. """
        # Arrange
        auth.login()

        filename = "test.txt"
        content = "test content"

        _get_response = mocker.MagicMock()
        _get_response.json.return_value = {
            "id": str(1),
            "name": filename,
            "file_path": "C:\\" + filename,
            "username": "admin",
            "uploaded": "Jan 1 2010",
        }

        _get_response_2 = mocker.MagicMock()
        _get_response_2.content = content

        mock_files_repo.get = mocker.MagicMock(
            side_effect=[_get_response, _get_response_2]
        )

        # Act
        response = client.get("/files/detail/1")

        # Assert
        assert response.status_code == 200
        assert b"test.txt" in response.data
        # assert b"test content" in response.data

        # ..get calls made to mock requests
        calls = mock_files_repo.get.call_args_list
        for call in calls:
            req = make_request(*call.args, **call.kwargs)

            assert req.url == files_service_url + "/files/1"
            assert req.headers == {
                "Authorization": auth_token,
            }

    def test_delete_file(
        self,
        client,
        app,
        auth,
        auth_token,
        mock_files_repo: MagicMock,
        files_service_url,
        make_request,
    ):
        """ Existing file can be deleted. """
        # Arrange
        auth.login()

        # Act
        response = client.post("/files/delete/1")

        # Assert
        assert response.status_code in [200, 302]

        calls = mock_files_repo.post.call_args_list
        for call in calls:
            req = make_request(*call.args, **call.kwargs)

            assert req.url == files_service_url + "/files/delete/1"
            assert req.headers == {
                "Authorization": auth_token,
            }
