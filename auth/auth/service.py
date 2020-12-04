"""
 * Project Name: RippedWebServer
 * File Name: service.py
 * Programmer: Kai Prince
 * Date: Sat, Nov 28, 2020
 * Description: This file contains service functions for the authentication app.
"""

from db.service import create_user, get_db
from werkzeug.security import check_password_hash
import auth.repository as repository
from authlib.jose import jwt
from flask import current_app
from datetime import timedelta
from time import time
from uuid import uuid4


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
    # breakpoint()

    requester_used_own_token = (
        str(requester_token_payload["sub"]).upper() == str(requester).upper()
    )
    requester_has_requested_permissions = all(
        x in requester_token_payload["permissions"] for x in requested_permissions
    )

    if requester_used_own_token and requester_has_requested_permissions:
        return True
    else:
        return False


def generate_resource_token(requester, file_path, duration: int, requested_permissions):
    audience = "public"
    duration = int(duration)

    token = jwt.encode(
        {"alg": "HS256", "typ": "JWT"},
        {
            "sub": file_path,
            "iss": requester,
            "aud": audience,
            "permissions": requested_permissions,
            "iat": int(time()),
            "exp": int(time()) + timedelta(seconds=duration).total_seconds(),
            "jti": str(uuid4()),
        },
        current_app.config["JWT_KEY"],
    ).decode("utf-8")

    return token
