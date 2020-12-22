from flask import Response, current_app

from auth.service import create_auth_token
from db.service import get_db
from service_api.disk_storage import make_repository


def get_disk_repo():
    base_url = current_app.config["DISK_STORAGE_SERVICE_URL"]
    auth_token = create_auth_token()

    return make_repository(base_url, auth_token)


def get_download_url(id) -> str:
    """ Consumes a file id and produces a url. """
    repo = get_db()
    db_file = repo.get_by_id(id)

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


def delete_file(id):
    """ Deletes a file from storage. """
    files_repo = get_db()

    file_path = files_repo.get_by_id(id)["file_path"]

    files_repo.delete(id)

    # Notify disk service
    disk_repo = get_disk_repo()
    disk_repo.delete(file_path)
