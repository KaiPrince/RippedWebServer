"""
 * Project Name: RippedWebServer
 * File Name: test_sharing_link.py
 * Programmer: Kai Prince
 * Date: Thu, Dec 03, 2020
 * Description: This file contains tests for creating links to share files.
"""


def test_sharing_link(
    client,
    mock_auth_repo,
    mock_files_repo,
    auth_token,
    auth,
    app,
    get_mock_request_call,
    auth_service_url,
    mocker,
):
    """ Share a file for 1 hour. """
    # Arrange
    auth.login()

    duration = 60 * 60 * 60
    file_path = "test.txt"
    file_id = "1"
    download_url = "http://example.com/storage/download/" + file_path
    sharing_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
    "eyJzdWIiOiJ0ZXN0LnR4dCIsImlzcyI6IjIiLCJhdWQiOiJwdWJsaW"
    "MiLCJwZXJtaXNzaW9ucyI6WyJyZWFkOiBkaXNrX3N0b3JhZ2UiXSwia"
    "WF0IjoxNjA3MDU2OTY0LCJleHAiOjE2MDcyNzI5NjQuMCwianRpIjoi"
    "ZTY5ZmZiNDQtODM3ZC00OGRiLWIwMDItNmNhZjhjMDRlMmYzIn0."
    "KCsmiOXO_Ak4YiYUuIZZlxm1KT1OfVXnDjstFWhCtVI"

    _get_response = mocker.MagicMock()
    _get_response.json.return_value = {
        "file_path": file_path,
        "download_url": download_url,
    }
    mock_files_repo.get.return_value = _get_response

    _post_response = mocker.MagicMock()
    _post_response.json.return_value = {"token": sharing_token}
    mock_auth_repo.post.return_value = _post_response

    # Act
    response = client.get(
        "/auth/generate_sharing_link",
        query_string={
            "duration": duration,
            "file_id": file_id,
        },
    )
    sharing_link = response.json["link"]

    # Assert
    assert (
        sharing_link
        == app.config["PUBLIC_FILES_SERVICE_URL"]
        + "/files/detail/"
        + file_id
        + "?token="
        + sharing_token
    )

    auth_repo_request = get_mock_request_call(mock_auth_repo.post)
    call = mock_auth_repo.post.call_args

    assert auth_repo_request.url == auth_service_url + "/auth/request_share_token"

    assert auth_repo_request.headers["Authorization"] == auth_token
    assert call.kwargs["json"] == {
        "requester": "1",
        "file_path": "test.txt",
        "duration": str(60 * 60 * 60),
        "permissions": ["read: files", "read: disk_storage"],
    }


def test_file_details(client):
    """File details view will allow the user anonymous access if they
    provide a sharing token."""

    # Arrange
    token = (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
        "eyJzdWIiOiJ0ZXN0LnR4dCIsImlzcyI6IjEiLCJhdWQiOi"
        "JwdWJsaWMiLCJwZXJtaXNzaW9ucyI6WyJyZWFkOiBmaWxlc"
        "yIsInJlYWQ6ZGlza19zdG9yYWdlIl19."
        "kMiBO47oHuMibmau5gBr8BjSvO16B-ZYQXmrGxO3F-U"
    )

    # Act
    response = client.get("/files/detail/1", query_string={"token": token})

    # Assert
    assert response.status_code == 200
    assert b"You are being granted temporary access" in response.data
