from flask import current_app, g

from files.service_api.disk_storage import IDiskStorageRepository
from files.service_api.disk_storage import make_repository as make_disk_repository
from files.service_api.files import IFilesRepository
from files.service_api.files import make_repository as make_files_repository

from .views import bp


@bp.before_app_request
def get_files_repository() -> IFilesRepository:
    base_url = current_app.config["FILES_SERVICE_URL"]
    auth_token = g.auth_token

    g.files_repo = make_files_repository(base_url, auth_token)


@bp.before_app_request
def get_disk_repository() -> IDiskStorageRepository:
    base_url = current_app.config["DISK_STORAGE_SERVICE_URL"]
    auth_token = g.auth_token

    g.disk_repo = make_disk_repository(base_url, auth_token)
