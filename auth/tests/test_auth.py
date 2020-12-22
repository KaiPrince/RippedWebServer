import pytest
from authlib.jose import jwt

from db.service import get_db


@pytest.mark.skip
def test_register(client, app):
    response = client.post("/auth/register", data={"username": "a", "password": "a"})
    assert "http://localhost/auth/login" == response.headers["Location"]

    with app.app_context():
        assert (
            get_db()
            .execute(
                "select * from user where username = 'a'",
            )
            .fetchone()
            is not None
        )


@pytest.mark.parametrize(
    ("username", "password", "user_id", "permissions"),
    [
        [
            "test",
            "test",
            1,
            [
                "read: files",
                "write: files",
                "read: disk_storage",
                "write: disk_storage",
            ],
        ],
        [
            "other",
            "othertest",
            2,
            [
                "read: files",
                "read: disk_storage",
            ],
        ],
    ],
)
def test_login(client, app, username, password, user_id, permissions):
    # Arrange

    # Act
    response = client.post(
        "/auth/login", json={"username": username, "password": password}
    )

    # Assert
    assert response.status_code == 200

    token = response.json["JWT"]

    claims = jwt.decode(
        token,
        app.secret_key,
    )

    assert claims["sub"] == user_id
    assert claims["name"] == username
    assert claims["permissions"] == permissions
