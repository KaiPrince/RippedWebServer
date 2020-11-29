"""
 * Project Name: RippedWebServer
 * File Name: service.py
 * Programmer: Kai Prince
 * Date: Sat, Nov 28, 2020
 * Description: This file contains service functions for the auth app.
"""

import requests
from flask import current_app
from authlib.jose import jwt


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


def get_user_data_from_auth_token(token) -> dict:
    body = jwt.decode(token, current_app.secret_key)

    return body
