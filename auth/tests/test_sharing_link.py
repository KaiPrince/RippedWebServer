"""
 * Project Name: RippedWebServer
 * File Name: test_sharing_link.py
 * Programmer: Kai Prince
 * Date: Wed, Dec 02, 2020
 * Description: This file contains tests for generating
 *   temporary or revokable tokens. 
 *   This will be used in the creation of sharing links.
"""
from uuid import uuid4

from authlib.jose import jwt
from pytest_mock import MockerFixture

from auth.service import validate_share_token_request


def test_generate_public_token(client, app, auth_token, mocker: MockerFixture):
    """Generate a token to publicly share a file that
    expires in 1 hour."""

    # Arrange
    file_path = "test.txt"
    requester = "2"
    duration = 60 * 60 * 60  # 1 hour
    secret_key = app.config["JWT_KEY"]
    permissions = ["read: disk_storage"]
    random_number = uuid4()

    # ..Mock the random number generator
    mocker.patch("auth.service.uuid4").return_value = random_number

    # Act
    response = client.post(
        "/auth/request_share_token",
        headers={"Authorization": auth_token},
        json={
            "requester": requester,
            "file_path": file_path,
            "duration": str(duration),
            "permissions": permissions,
        },
    )

    token = response.json["token"]

    # Assert

    # ..Decode generated token
    # ..(Throws if invalid)
    token_payload = jwt.decode(token, secret_key)

    assert token_payload["sub"] == file_path
    assert token_payload["aud"] == "public"
    assert int(token_payload["exp"]) - int(token_payload["iat"]) == duration
    assert token_payload["iss"] == requester
    assert token_payload["jti"] == str(random_number)
    assert token_payload["permissions"] == permissions


class TestUnits:
    """ Contains unit tests for the sharing feature. """

    def test_validate_request(self):
        """Only allows valid requests.
        The requester must use his own token.
        The requester must have the permissions he wishes to extend.
        """

        # Arrange
        user_token = {
            "sub": "1",
            "name": "test",
            "permissions": ["read: files", "read: disk_storage"],
            "iat": 1516239022,
        }
        requester = "1"
        requested_permissions = ["read: disk_storage"]

        # Act
        is_valid = validate_share_token_request(
            user_token, requester, requested_permissions
        )

        # Assert
        assert is_valid is True
