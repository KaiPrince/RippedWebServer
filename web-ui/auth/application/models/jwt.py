"""
 * Project Name: RippedWebServer
 * File Name: jwt.py
 * Programmer: Kai Prince
 * Date: Sat, Feb 06, 2021
 * Description: This file contains JWT decoding functions.
"""

from authlib.jose import jwt
from flask import current_app


def get_payload_from_auth_token(token) -> dict:
    body = jwt.decode(token, current_app.config["JWT_KEY"])

    return body
