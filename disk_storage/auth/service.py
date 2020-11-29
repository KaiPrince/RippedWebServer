"""
 * Project Name: RippedWebServer
 * File Name: service.py
 * Programmer: Kai Prince
 * Date: Sat, Nov 28, 2020
 * Description: This file contains service functions for the auth module.
"""

from authlib.jose.errors import AuthlibBaseError
from authlib.jose import jwt
from flask import current_app


def decode_auth_token(token: str) -> dict:
    try:
        return jwt.decode(token, current_app.config["JWT_KEY"])
    except AuthlibBaseError:
        raise RuntimeError()
