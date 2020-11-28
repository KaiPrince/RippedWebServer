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


def find_user(username: str) -> dict:
    return repository.find_user(username)


def does_password_match(guessed: str, stored: str) -> bool:
    return check_password_hash(stored, guessed)


def get_user_permissions(user_id: int) -> list:
    rows = repository.get_permissions_by_user_id(user_id)

    permissions = [x["access_level"] + ": " + x["scope"] for x in rows]

    return permissions
