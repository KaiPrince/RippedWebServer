"""
 * Project Name: RippedWebServer
 * File Name: models.py
 * Programmer: Kai Prince
 * Date: Mon, Dec 07, 2020
 * Description: This file contains model definitions for the auth app.
"""

from datetime import datetime
from typing import List, Literal


class Permission:
    """
    * Class Name: Permission
    * Purpose: This purpose of this class is to define the properties
    *  of the Permission entity.
    *  A permission is used authorize certain actions.
    """

    operation: Literal["read", "write"]
    scope: Literal["files", "disk_storage"]

    def __init__(self, operation, scope):
        self.operation = operation
        self.scope = scope

    @staticmethod
    def from_string(string: str):
        operation, scope = [x.strip() for x in string.split(":")]

        instance = Permission(operation, scope)

        # TODO add validation

        return instance

    def __eq__(self, other):
        is_equal = self.operation == other.operation and self.scope == other.scope

        return is_equal


class AuthTicket:
    """
    * Class Name: AuthTicket
    * Purpose: This purpose of this class is to define the properties
    *  of the AuthTicket entity.
    *  An AuthTicket is used to grant its holder access to specific resources.
    """

    subject: str
    issuer: str
    audience: str
    issued_at: datetime
    expires_at: datetime
    unique_id: str
    permissions: List[Permission]

    def __init__(
        self,
        subject,
        issuer,
        audience,
        issued_at,
        expires_at,
        unique_id,
        permissions,
    ):

        if subject is None:
            raise ValueError("Subject must be defined.")

        self.subject = subject
        self.issuer = issuer
        self.audience = audience
        self.issued_at = issued_at
        self.expires_at = expires_at
        self.unique_id = unique_id
        self.permissions = permissions

    @staticmethod
    def from_jwt(json: dict):

        (subject, issuer, audience, issued_at, expires_at, unique_id, permissions,) = [
            json.get(x)
            for x in [
                "sub",
                "iss",
                "aud",
                "iat",
                "exp",
                "jti",
                "permissions",
            ]
        ]

        if not isinstance(permissions, list):
            raise ValueError("permissions was not a valid list")

        permissions = [Permission.from_string(permission) for permission in permissions]

        instance = AuthTicket(
            subject,
            issuer,
            audience,
            issued_at,
            expires_at,
            unique_id,
            permissions,
        )

        return instance
