"""
 * Project Name: RippedWebServer
 * File Name: service.py
 * Programmer: Kai Prince
 * Date: Sat, Nov 28, 2020
 * Description: This file contains service functions for the auth module.
"""

from datetime import timedelta
from time import time

from authlib.jose import jwt
from authlib.jose.errors import AuthlibBaseError
from flask import current_app


def decode_auth_token(token: str) -> dict:
    try:
        claim = jwt.decode(token, current_app.config["JWT_KEY"])
        claim.validate()

        return claim
    except AuthlibBaseError:
        raise RuntimeError()


def create_auth_token():
    # TODO Delete this and use the auth service!
    # or better yet install a pub/sub message broker
    header = {"alg": "HS256"}

    payload = {
        "permissions": ["write: disk_storage"],
        "iat": int(time()),
        "exp": int(time()) + timedelta(hours=1).total_seconds(),
    }

    key = current_app.config["JWT_KEY"]
    token = jwt.encode(header, payload, key).decode("utf-8")

    return token
