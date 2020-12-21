"""
 * Project Name: RippedWebServer
 * File Name: sql.py
 * Programmer: Kai Prince
 * Date: Sun, Dec 13, 2020
 * Description: This file contains an SQL implementation of the Files Repository.
"""

from . import IFilesRepository


class FilesSqlRepository(IFilesRepository):
    def __init__(self, db):
        self.db = db

    def index(self):
        db = self.db

        files = db.execute(
            "SELECT f.id, file_name, uploaded, user_id, file_path"
            " FROM user_file f"
            " ORDER BY uploaded DESC"
        ).fetchall()

        files_array = list(dict(x) for x in files)
        return files_array

    def get_by_id(self, id):
        """ Consumes an ID and produces file details. """
        db = self.db

        db_file = db.execute(
            "SELECT f.id, file_name as name, uploaded, user_id, file_path"
            " FROM user_file f"
            " WHERE f.id = ?"
            " ORDER BY uploaded DESC",
            [str(id)],
        ).fetchone()

        if not db_file:
            return None

        return dict(db_file)

    def search(self, predicate):
        raise NotImplementedError

    def create(self, file_name, user_id, file_path):
        db = self.db

        db_cursor = db.execute(
            "INSERT INTO user_file (file_name, user_id, file_path)" " VALUES (?, ?, ?)",
            (file_name, user_id, file_path),
        )
        db.commit()

        return db_cursor.lastrowid

    def edit(self, file_id, file_name, user_id, file_path):
        raise NotImplementedError

    def delete(self, file_id):
        db = self.db
        db.execute("DELETE from user_file" " WHERE id = ?", [str(file_id)])
        db.commit()


def make_files_sql_repo(db):
    return FilesSqlRepository(db)
