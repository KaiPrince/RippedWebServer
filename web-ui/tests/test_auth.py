from unittest.mock import MagicMock

import pytest
from authlib.jose import jwt
from flask import session

from auth.permissions import make_jwt_permissions_reader


@pytest.mark.skip
def test_register(client, app):
    assert client.get("/auth/register").status_code == 200
    response = client.post("/auth/register", data={"username": "a", "password": "a"})
    assert "http://localhost/auth/login" == response.headers["Location"]

    # with app.app_context():
    #     assert (
    #         get_db()
    #         .execute(
    #             "select * from user where username = 'a'",
    #         )
    #         .fetchone()
    #         is not None
    #     )


@pytest.mark.skip
@pytest.mark.parametrize(
    ("username", "password", "message"),
    (
        ("", "", b"Username is required."),
        ("a", "", b"Password is required."),
    ),
)
def test_register_validate_input(client, username, password, message):
    response = client.post(
        "/auth/register", data={"username": username, "password": password}
    )
    assert message in response.data


@pytest.mark.parametrize(
    ("username", "password"),
    [
        ["test", "test"],
        ["other", "othertest"],
    ],
)
def test_login(
    app, client, mock_auth_repo: MagicMock, auth_service_url, username, password, mocker
):
    # Arrange

    mock_token = jwt.encode(
        {"alg": "HS256"},
        {"sub": 2, "name": username, "permissions": ""},
        app.secret_key,
    ).decode("utf-8")

    _get_response = mocker.MagicMock()
    _get_response.json.return_value = {"JWT": mock_token}

    mock_auth_repo.post.return_value = _get_response

    # Act
    client.post("/auth/login", data={"username": username, "password": password})

    # Assert
    mock_auth_repo.post.assert_called_once_with(
        auth_service_url + "/auth/login",
        json={"username": username, "password": password},
    )

    # ..The user data is stored in the session
    # TODO
    # with app.test_request_context(
    #     "/auth/login", data={"username": username, "password": password}
    # ):
    #     assert session["user"] == {"user_id": 2}


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert "user_id" not in session


class TestPermissionsReader:
    """
    * Class Name: TestPermissions
    * Purpose: This purpose of this class is to test the PermissionsReader
    *  classes.
    """

    @pytest.mark.parametrize(
        ("payload", "resource", "expected"),
        [
            (
                {
                    "sub": "test.txt",
                    "iss": "1",
                    "aud": "public",
                    "permissions": ["read: files", "read:disk_storage"],
                },
                "test.txt",
                False,
            ),
            (
                {
                    "sub": "test.txt",
                    "iss": "1",
                    "aud": "public",
                    "permissions": ["write: files", "write:disk_storage"],
                },
                "test.txt",
                True,
            ),
            (
                {
                    "sub": "test.txt",
                    "iss": "1",
                    "aud": "public",
                    "permissions": ["write: files", "write:disk_storage"],
                },
                "otherfile.txt",
                False,
            ),
            (
                {
                    "sub": "2",
                    "name": "test",
                    "permissions": ["write: files", "write: disk_storage"],
                    "iat": 1516239022,
                },
                "otherfile.txt",
                True,
            ),
            (
                {
                    "sub": "test.txt",
                    "iss": "1",
                    "aud": "public",
                    "permissions": ["write: files"],
                },
                "test.txt",
                False,
            ),
            (
                {
                    "sub": "test.txt",
                    "iss": "1",
                    "aud": "public",
                    "permissions": ["write: disk_storage"],
                },
                "test.txt",
                False,
            ),
        ],
    )
    def test_may_delete(self, payload, resource, expected):
        # Arrange
        auth_token = payload

        # Act
        may_delete = make_jwt_permissions_reader(auth_token).may_delete(resource)

        # Assert
        assert may_delete is expected

    @pytest.mark.parametrize(
        ("payload", "resource", "expected"),
        [
            (
                {
                    "sub": "test.txt",
                    "iss": "1",
                    "aud": "public",
                    "permissions": ["read: files", "read:disk_storage"],
                },
                "test.txt",
                False,
            ),
            (
                {
                    "sub": "test.txt",
                    "iss": "1",
                    "aud": "public",
                    "permissions": ["write: files", "write:disk_storage"],
                },
                "test.txt",
                False,
            ),
            (
                {
                    "sub": "test.txt",
                    "iss": "1",
                    "aud": "public",
                    "permissions": ["write: files", "write:disk_storage"],
                },
                "otherfile.txt",
                False,
            ),
            (
                {
                    "sub": "2",
                    "name": "test",
                    "permissions": ["read: files", "read: disk_storage"],
                    "iat": 1516239022,
                },
                "otherfile.txt",
                True,
            ),
            (
                {
                    "sub": "2",
                    "name": "test",
                    "permissions": ["read: files"],
                    "iat": 1516239022,
                },
                "otherfile.txt",
                True,
            ),
            (
                {
                    "sub": "2",
                    "name": "test",
                    "permissions": ["write: files", "write: disk_storage"],
                    "iat": 1516239022,
                },
                "otherfile.txt",
                False,
            ),
            (
                {
                    "sub": "test.txt",
                    "iss": "1",
                    "aud": "public",
                    "permissions": ["write: files"],
                },
                "test.txt",
                False,
            ),
            (
                {
                    "sub": "test.txt",
                    "iss": "1",
                    "aud": "public",
                    "permissions": ["write: disk_storage"],
                },
                "test.txt",
                False,
            ),
        ],
    )
    def test_may_share(self, payload, resource, expected):
        # Arrange
        auth_token = payload

        # Act
        may_share = make_jwt_permissions_reader(auth_token).may_share(resource)

        # Assert
        assert may_share is expected
