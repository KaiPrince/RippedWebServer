"""
 * Project Name: RippedWebServer
 * File Name: auth.py
 * Programmer: Kai Prince
 * Date: Sat, Feb 06, 2021
 * Description: This file contains the outbound auth service port.
"""


from requests.exceptions import HTTPError
from flask import current_app
from auth.adapter.outbound.service_api import auth
from auth.adapter.inbound.jwt.decode import get_payload_from_auth_token


def get_auth_token(username, password) -> dict:
    auth_token = None

    try:
        auth_token = auth.get_auth_token(username, password)

        payload = get_payload_from_auth_token(auth_token)
        current_app.logger.debug(
            "Log in successful. "
            + str(
                {
                    "username": payload["name"],
                    "id": payload["sub"],
                    "auth_token": auth_token,
                }
            )
        )

    except HTTPError as e:
        # TODO handle different errors (e.g. Server failure)

        current_app.logger.debug(
            "Log in failed. " + str({"status_code": e.response.status_code})
        )

    return auth_token


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

    # TODO Get requestor from own_token
    # TODO Get file_path from shared_resource
    return auth.request_share_token(
        own_token, "1", "test.txt", duration, requested_permissions
    )
