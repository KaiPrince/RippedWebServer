import os
from db.service import get_db
from flask import current_app
import logging


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


def delete_file(id):
    """ Deletes a file from storage. """

    db = get_db()

    db_file = get_file(id)

    file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], db_file)

    try:
        db.execute("DELETE from user_file" " WHERE id = ?", str(id))

        os.remove(file_path)
    except FileNotFoundError as e:
        logging.error(f"Failed to delete {file_path}.", exc_info=e)
    finally:
        db.commit()