"""
 * Project Name: RippedWebServer
 * user Name: sql.py
 * Programmer: Kai Prince
 * Date: Sun, Dec 13, 2020
 * Description: This user contains an SQL implementation of the users Repository.
"""

from sqlite3 import Connection

from . import IUsersRepository


class UsersSqlRepository(IUsersRepository):
    def __init__(self, db: Connection):
        self.db = db

    def __del__(self):
        self.db.close()

    def index(self):
        db = self.db

        users = db.execute("SELECT * FROM user").fetchall()
        users = [self._db_user_to_dict(x) for x in users]

        users_with_permissions = [
            {
                **x,
                "permissions": [
                    self._conform_permission(y)
                    for y in self._get_user_permissions(x["id"])
                ],
            }
            for x in users
        ]
        return users_with_permissions

    def get_by_id(self, user_id):
        """ Consumes an ID and produces user details. """
        user = self.db.execute(
            "SELECT * FROM user WHERE id = ?",
            [user_id],
        ).fetchone()
        user = self._db_user_to_dict(user)

        user_with_permissions = {
            **user,
            "permissions": [
                self._conform_permission(y) for y in self._get_user_permissions(user["id"])
            ],
        }
        return user_with_permissions

    def get_by_username(self, username: str) -> dict:
        user = self.db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()

        user = self._db_user_to_dict(user)

        user_with_permissions = {
            **user,
            "permissions": self._get_user_permissions(user["id"]),
        }
        return user_with_permissions

    def search(self, predicate):
        all_items = self.index()
        search_results = [x for x in all_items if predicate(x)]

        return search_results

    def create(self, username, password, permissions):

        db = self.db

        db_cursor = db.execute(
            "INSERT INTO user (username, password) VALUES (?, ?)",
            (username, password),
        )
        db.commit()

        user_id = db_cursor.lastrowid

        for permission in permissions:
            access_level = permission["access_level"]
            scope = permission["scope"]
            permission_id = self._get_permission(access_level, scope)["id"]

            db.execute(
                "INSERT INTO user_permissions (user_id, permission_id) "
                "VALUES (?, ?)",
                [user_id, permission_id],
            )
            db.commit()

        return user_id

    def edit(self, user_id, password, permissions):
        raise NotImplementedError

    def delete(self, user_id):
        db = self.db
        db.execute("DELETE from user" " WHERE id = ?", [str(user_id)])
        db.commit()

    def _db_user_to_dict(self, db_user: tuple) -> dict:
        if isinstance(db_user, dict):
            return db_user

        user_details = {
            "id": db_user[0],
            "username": db_user[1],
            "password": db_user[2],
        }

        return user_details

    def _db_permission_to_dict(self, db_permission: tuple) -> dict:
        if isinstance(db_permission, dict):
            return db_permission

        details = {
            "id": db_permission[0],
            "access_level": db_permission[1],
            "scope": db_permission[2],
        }

        return details

    def _conform_permission(self, record: dict) -> dict:
        if record is None:
            return record

        result = {**record}
        result.pop("id", None)

        return result

    def _get_user_permissions(self, user_id) -> dict:
        raw_permissions = self.db.execute(
            "SELECT permission.id, access_level, scope FROM permission"
            " JOIN user_permissions"
            " ON permission.id=user_permissions.permission_id"
            " WHERE user_permissions.user_id = ?",
            [user_id],
        ).fetchall()

        permissions = [self._db_permission_to_dict(x) for x in raw_permissions]
        return permissions

    def _get_all_permissions(self) -> dict:
        permissions = self.db.execute(
            "SELECT id, access_level, scope FROM permission"
        ).fetchall()
        permissions = [self._db_permission_to_dict(x) for x in permissions]

        return permissions

    def _get_permission(self, access_level, scope):
        permissions = self._get_all_permissions()

        result = [
            x
            for x in permissions
            if x["access_level"] == access_level and x["scope"] == scope
        ][0]

        return result


def make_users_sql_repo(db):
    return UsersSqlRepository(db)
