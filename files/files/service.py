from db.service import get_db
from flask import current_app

import files.repository as repository


def get_file(id):
    """ Consumes an ID and produces file details. """

    db = get_db()
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


def get_file_content(id):
    """ Consumes an ID and produces a byte stream or bytes. """

    file_path = get_file(id)["file_path"]

    return repository.get_file_content(file_path)


def create_file(file_name, file_size):
    current_app.logger.debug(
        "create_file " + str({"file_name": file_name, "file_size": file_size}),
    )

    response = repository.create_file(file_name, file_size)

    response.raise_for_status()

    return response


def put_file(file_path, content_range, content_total, content):
    # Append to file
    current_app.logger.debug(
        "put_file "
        + str(
            {
                "file_path": file_path,
                "content_range": content_range,
                "content_total": content_total,
            }
        ),
    )

    response = repository.put_file(file_path, content_range, content_total, content)

    response.raise_for_status()

    return response.json()["file_size"]


def delete_file(id):
    """ Deletes a file from storage. """

    db = get_db()

    file_path = get_file(id)["file_path"]

    repository.delete_file(file_path)

    db.execute("DELETE from user_file" " WHERE id = ?", [str(id)])

    db.commit()
