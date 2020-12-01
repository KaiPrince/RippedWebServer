from unittest.mock import MagicMock

import pytest
from authlib.jose import jwt
from flask import session


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
