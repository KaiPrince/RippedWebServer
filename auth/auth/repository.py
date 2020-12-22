"""
 * Project Name: RippedWebServer
 * File Name: repository.py
 * Programmer: Kai Prince
 * Date: Sat, Nov 28, 2020
 * Description: This file contains repository-level functions for the auth app.
"""

from sqlite3 import Row

from db.service import get_db


def find_user(username: str) -> Row:
    db = get_db()

    return db.execute("SELECT * FROM user WHERE username = ?", (username,)).fetchone()


def get_permissions_by_user_id(user_id: int) -> Row:
    db = get_db()

    return db.execute(
        "SELECT access_level, scope FROM permission JOIN user_permissions ON"
        " permission.id=user_permissions.permission_id"
        " WHERE user_permissions.user_id = ?",
        [user_id],
    ).fetchall()
