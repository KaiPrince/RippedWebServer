"""
 * Project Name: RippedWebServer
 * File Name: service.py
 * Programmer: Kai Prince
 * Date: Sat, Nov 28, 2020
 * Description: This file contains service functions for the auth app.
"""

from time import time

import requests
from authlib.jose import jwt
from flask import current_app


def _base_url():
    return current_app.config["AUTH_SERVICE_URL"]


def get_auth_token(username, password) -> dict:
    response = requests.post(
        f"{_base_url()}/auth/login",
        json={
            # TODO This is a terrible security problem! Encrypt this first
            "username": username,
            "password": password,
        },
    )

    response.raise_for_status()

    json = response.json()

    token = json["JWT"]
    return token


def get_payload_from_auth_token(token) -> dict:
    body = jwt.decode(token, current_app.config["JWT_KEY"])

    return body


def is_token_expired(token) -> bool:
    if "exp" in token:
        expiry = token["exp"]
        now = int(time())
        return now > expiry
    else:
        return False


def request_share_token(
    own_token: str,
    shared_resource: str,
    duration: int,
    requested_permissions: list,
):
    """Consumes an auth token, a resource to provide access to
    such as a file path, the requested duration (in seconds), and the requested
    permissions.
    """

    # TODO inject this instead
    base_url = current_app.config["AUTH_SERVICE_URL"]

    response = requests.post(
        base_url + "/auth/request_share_token",
        headers={"Authorization": own_token},
        json={
            "requester": "1",
            "file_path": "test.txt",
            "duration": str(60 * 60 * 60),
            "permissions": requested_permissions,
        },
    )

    response.raise_for_status()

    share_token = response.json()["token"]

    return share_token
