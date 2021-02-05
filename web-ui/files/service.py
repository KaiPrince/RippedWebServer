from flask import current_app, flash, g, redirect, session, url_for
from requests import ConnectionError, HTTPError
from werkzeug.exceptions import abort

from files.service_api.disk_storage import IDiskStorageRepository
from files.service_api.disk_storage import \
    make_repository as make_disk_repository
from files.service_api.files import IFilesRepository
from files.service_api.files import make_repository as make_files_repository


def get_repository() -> IFilesRepository:
    base_url = current_app.config["FILES_SERVICE_URL"]
    auth_token = g.auth_token

    return make_files_repository(base_url, auth_token)


def get_disk_repository() -> IDiskStorageRepository:
    base_url = current_app.config["DISK_STORAGE_SERVICE_URL"]
    auth_token = g.auth_token

    return make_disk_repository(base_url, auth_token)


def get_index():
    """ Consumes nothing and produces a list of files. """

    repository = get_repository()

    try:
        files = repository.index()
    except (HTTPError, ConnectionError):
        # TODO move library-specific errors to repo and make custom errors
        flash("Could not retrieve file index.", category="error")
        files = []

    return files


def get_file(id):
    """ Consumes an ID and produces a file name. """

    repository = get_repository()

    return repository.get_by_id(id)


def get_download_url(id):
    file = get_file(id)
    current_app.logger.debug("Download URL got file " + str(file))

    return file["download_url"]


def upload_file(file_name, file_path, content_range, content_total, file):
    """ Consumes file data and produces a Response. """

    if "file_id" not in session:
        current_app.logger.debug(
            "File Id not found on session. This must be the first packet."
        )
        # ..Send create request on first packet.
        # TODO pass total size and check free disk space
        file_id = create_file(file_name, g.user["id"], file_path, content_total)

        if not file_id:
            flash("Couldn't create new file.", category="error")
            return abort(500)

        session["file_id"] = file_id
    else:
        current_app.logger.debug(
            "File Id found on session. "
            + str({"file_id": session["file_id"], "session": session}),
        )
        file_id = session["file_id"]

    put_file(file_id, content_range, content_total, file)

    # Clean session
    content_range_end = int(content_range.split("-")[-1])
    if content_range_end >= int(content_total) - 1:
        current_app.logger.debug("Final packet recieved.")
        session.pop("file_id", None)
        current_app.logger.debug(
            "Removed File Id from session. " + str({"session": session})
        )

        return redirect(url_for("files.index"))

    return {"files": [{"name": file_name}]}


def create_file(file_name, user_id, file_path, content_total):
    """ Consumes file details and produces a file id. """
    current_app.logger.debug(
        "create_file "
        + str({"file_name": file_name, "user_id": user_id, "file_path": file_path}),
    )

    repository = get_repository()

    file_id = repository.create(file_name, user_id, file_path, content_total)

    return file_id


def put_file(file_id, content_range, content_total, content):
    """Consumes a file id, file content and content-range,
    and produces a file size."""

    files_repo = get_repository()
    file_path = files_repo.get_by_id(file_id)["file_path"]

    if file_path is None:
        return 0

    repository = get_disk_repository()
    file_size = repository.write(file_path, content_range, content_total, content)

    current_app.logger.debug(
        "put_file "
        + str(
            {
                "file_id": file_id,
                "content_range": content_range,
                "content_total": content_total,
                "current size": file_size,
            }
        ),
    )
    return file_size


def delete_file(id):
    """ Deletes a file from storage. """
    repository = get_repository()

    return repository.delete(id)
