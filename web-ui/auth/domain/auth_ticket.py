"""
 * Project Name: RippedWebServer
 * File Name: auth_ticket.py
 * Programmer: Kai Prince
 * Date: Fri, Feb 05, 2021
 * Description: This file contains the AuthTicket model.
"""

from time import time
from datetime import datetime
from typing import List  # , Literal

from .permission import Permission


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

    def is_expired(self) -> bool:
        if self.expires_at:
            now = int(time())
            return now > self.expires_at
        else:
            return False

    # TODO Sort out terminology: jwt, ticket, token, claims
    @staticmethod
    def from_claims(json: dict):

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

    def to_jwt(self):
        json: dict = dict()

        permissions = [str(x) for x in self.permissions]

        for x, y in [
            ("sub", self.subject),
            ("iss", self.issuer),
            ("aud", self.audience),
            ("iat", self.issued_at),
            ("exp", self.expires_at),
            ("jti", self.unique_id),
            ("permissions", permissions),
        ]:
            json[x] = y

        return json
