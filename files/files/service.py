from db.service import get_db
from flask import current_app, Response

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


def get_download_url(id) -> str:
    """ Consumes a file id and produces a url. """
    db_file = get_file(id)

    if db_file is None or "file_path" not in db_file.keys():
        return None

    file_path = db_file["file_path"]

    return build_download_url(file_path)


def build_download_url(file_path: str) -> str:
    """ Consumes a file path and returns a full url. """

    url_path = f"/storage/download/{file_path}"
    url_base = current_app.config["PUBLIC_DISK_STORAGE_SERVICE_URL"]

    url = url_base + url_path

    return url


def build_upload_url(file_path: str) -> str:
    """ Consumes a file path and returns a full url. """

    url_path = f"/storage/create/{file_path}"
    url_base = current_app.config["PUBLIC_DISK_STORAGE_SERVICE_URL"]

    url = url_base + url_path

    return url


def download_file(file_path) -> Response:
    """ Consumes a file path and produces a response which includes the file. """

    r = repository.download_file(file_path)
    headers = dict(r.raw.headers)

    def generate():
        for chunk in r.raw.stream(decode_content=False):
            yield chunk

    out = Response(generate(), headers=headers)
    out.status_code = r.status_code

    return out


def delete_file(id):
    """ Deletes a file from storage. """

    db = get_db()

    file_path = get_file(id)["file_path"]

    repository.delete_file(file_path)

    db.execute("DELETE from user_file" " WHERE id = ?", [str(id)])

    db.commit()
