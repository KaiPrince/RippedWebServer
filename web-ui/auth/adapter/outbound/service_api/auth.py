"""
 * Project Name: RippedWebServer
 * File Name: auth.py
 * Programmer: Kai Prince
 * Date: Sat, Feb 06, 2021
 * Description: This file contains the outbound auth service adapter.
"""


import requests

from . import _base_url


def fetch_auth_token(username, password) -> str:
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


def request_share_token(
    own_token: str,
    requester: str,
    file_path: str,
    duration: int,
    requested_permissions: list,
):
    """Consumes an auth token, a resource to provide access to
    such as a file path, the requested duration (in seconds), and the requested
    permissions.
    """

    response = requests.post(
        _base_url() + "/auth/request_share_token",
        headers={"Authorization": own_token},
        json={
            "requester": requester,
            "file_path": file_path,
            "duration": duration,
            "permissions": requested_permissions,
        },
    )

    response.raise_for_status()

    share_token = response.json()["token"]

    return share_token
