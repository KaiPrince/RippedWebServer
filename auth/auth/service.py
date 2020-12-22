"""
 * Project Name: RippedWebServer
 * File Name: service.py
 * Programmer: Kai Prince
 * Date: Sat, Nov 28, 2020
 * Description: This file contains service functions for the authentication app.
"""

from datetime import timedelta
from time import time
from uuid import uuid4

from authlib.jose import jwt
from flask import current_app
from werkzeug.security import check_password_hash

import auth.repository as repository
from db.service import create_user, get_db


def find_user(username: str) -> dict:
    return repository.find_user(username)


def does_password_match(guessed: str, stored: str) -> bool:
    return check_password_hash(stored, guessed)


def get_user_permissions(user_id: int) -> list:
    rows = repository.get_permissions_by_user_id(user_id)

    permissions = [x["access_level"] + ": " + x["scope"] for x in rows]

    return permissions


def get_token_payload(token):
    secret_key = current_app.config["JWT_KEY"]
    token_payload = jwt.decode(token, secret_key)

    return token_payload


def validate_share_token_request(
    requester_token_payload, requester, requested_permissions
):
    """Consumes a token payload, a requester id, and a list of permissions,
    and produces a boolean."""

    token_subject = str(requester_token_payload["sub"]).casefold()
    requester = str(requester).casefold()
    token_permissions = [
        str(x).casefold() for x in requester_token_payload["permissions"]
    ]

    # Validate
    requester_used_own_token = token_subject == requester
    requester_has_requested_permissions = all(
        x in token_permissions for x in requested_permissions
    )

    is_valid = requester_used_own_token and requester_has_requested_permissions

    return is_valid


def generate_resource_token(requester, file_path, duration: int, requested_permissions):
    duration = int(duration)

    subject = file_path
    issuer = requester
    audience = "public"
    permissions = requested_permissions
    issued_at = int(time())
    expires_at = issued_at + timedelta(seconds=duration).total_seconds()
    token_id = str(uuid4())
    secret = current_app.config["JWT_KEY"]

    token = jwt.encode(
        {"alg": "HS256", "typ": "JWT"},
        {
            "sub": subject,
            "iss": issuer,
            "aud": audience,
            "permissions": permissions,
            "iat": issued_at,
            "exp": expires_at,
            "jti": token_id,
        },
        secret,
    ).decode("utf-8")

    return token
