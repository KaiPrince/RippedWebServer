"""
 * Project Name: RippedWebServer
 * File Name: test_auth.py
 * Programmer: Kai Prince
 * Date: Sun, Nov 29, 2020
 * Description: This file contains authorization tests.
"""


class TestAuth:
    def test_auth_token_required(self, client):
        # Arrange
        # Act
        response = client.get(
            "/files/",
        )

        # Assert
        assert response.status_code == 401

    def test_bad_auth_token(self, client):
        # Arrange
        # Act
        response = client.get(
            "/files/", headers={"Authorization": "thisisafakeauthtoken"}
        )

        # Assert
        assert response.status_code == 401

    def test_index(self, client, auth_token):
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
        assert response.status_code == 200
        assert b"test.txt" in response.data
