"""
 * Project Name: RippedWebServer
 * File Name: test_entities.py
 * Programmer: Kai Prince
 * Date: Mon, Dec 07, 2020
 * Description: This file contains tests for entity models.
"""

import pytest
from auth.models import AuthTicket, Permission


@pytest.mark.parametrize(
    (
        "json",
        "subject",
        "issuer",
        "audience",
        "issued_at",
        "expires_at",
        "unique_id",
        "permissions",
    ),
    [
        (
            {
                "sub": "2",
                "name": "test",
                "iss": "2",
                "iat": 1516239022,
                "jti": "123456",
                "permissions": ["read: files", "write: files"],
            },
            "2",
            "2",
            None,
            1516239022,
            None,
            "123456",
            [Permission("read", "files"), Permission("write", "files")],
        ),
        (
            {
                "sub": "test.txt",
                "iss": "1",
                "aud": "public",
                "permissions": ["read: files", "read:disk_storage"],
            },
            "test.txt",
            "1",
            "public",
            None,
            None,
            None,
            [Permission("read", "files"), Permission("read", "disk_storage")],
        ),
        (
            {
                "sub": "test.txt",
                "iss": "1",
                "aud": "public",
                "permissions": ["read: files", "read: disk_storage"],
                "iat": 1607275408,
                "exp": 1607491408,
                "jti": "0ddea700-78d4-4c0c-9a1e-18c0d9d62b96",
            },
            "test.txt",
            "1",
            "public",
            1607275408,
            1607491408,
            "0ddea700-78d4-4c0c-9a1e-18c0d9d62b96",
            [Permission("read", "files"), Permission("read", "disk_storage")],
        ),
        (
            {
                "sub": "test.txt",
                "iss": "1",
                "aud": "public",
                "permissions": [],
                "iat": 1607275408,
                "exp": 1607491408,
                "jti": "0ddea700-78d4-4c0c-9a1e-18c0d9d62b96",
            },
            "test.txt",
            "1",
            "public",
            1607275408,
            1607491408,
            "0ddea700-78d4-4c0c-9a1e-18c0d9d62b96",
            [],
        ),
    ],
)
def test_auth_ticket_from_dict(
    json,
    subject,
    issuer,
    audience,
    issued_at,
    expires_at,
    unique_id,
    permissions,
):
    # Arrange

    # Act
    instance = AuthTicket.from_jwt(json)

    # Assert

    assert instance.subject == subject
    assert instance.issuer == issuer
    assert instance.audience == audience
    assert instance.issued_at == issued_at
    assert instance.expires_at == expires_at
    assert instance.unique_id == unique_id
    assert instance.permissions == permissions


@pytest.mark.parametrize(
    ("json"),
    [
        {
            "sub": "test.txt",
            "iss": "1",
            "aud": "public",
            "permissions": ["rles", "reastorage"],
        },
        {
            "sub": "test.txt",
            "iss": "1",
            "aud": "public",
            "permissions": "fasgas",
        },
        {
            "permissions": ["read: files", "read: disk_storage"],
        },
    ],
)
def test_auth_ticket_from_bad_jwt(json):
    # Arrange

    # Act
    with pytest.raises(ValueError):
        AuthTicket.from_jwt(json)

    # Assert


@pytest.mark.parametrize(
    ("string", "operation", "scope"),
    [
        ("read: files", "read", "files"),
        ("read: disk_storage", "read", "disk_storage"),
        ("write: files", "write", "files"),
        ("write: disk_storage", "write", "disk_storage"),
    ],
)
def test_permissions_from_string(string, operation, scope):
    # Arrange

    # Act
    instance = Permission.from_string(string)

    # Assert
    assert instance.operation == operation
    assert instance.scope == scope
