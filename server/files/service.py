from db.service import get_db


def get_file(id):
    """ Consumes an ID and produces a file name. """

    db = get_db()
    db_file = db.execute(
        "SELECT f.id, file_name as name, uploaded, user_id, username, file_path"
        " FROM user_file f JOIN user u ON f.user_id = u.id"
        " WHERE f.id = ?"
        " ORDER BY uploaded DESC",
        str(id),
    ).fetchone()

    if not db_file:
        return None

    return db_file["file_path"]
