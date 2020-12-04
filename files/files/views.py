from flask import Blueprint, current_app, make_response, request
from flask.helpers import NotFound
from requests import HTTPError
from werkzeug.utils import secure_filename
from werkzeug.exceptions import abort

import files.service as service
from auth.middleware import permission_required
from db.files import make_files_sql_repo as get_files_repo
from operator import itemgetter

# from .utils import allowed_file


bp = Blueprint("files", __name__, url_prefix="/files", template_folder="templates")


@bp.route("/")
# @permission_required("list: files")
def index():
    repo = get_files_repo()

    files: list = repo.index()

    for file in files:
        file["download_url"] = service.build_download_url(file["file_path"])
        file["upload_url"] = service.build_upload_url(file["file_path"])

    return {"files": files}


@bp.route("/create", methods=["POST"])
@permission_required("write: files")
def create():
    json = request.json

    # Get params
    required_params = ["user_id", "file_name", "file_path", "content_total"]
    if any(x not in json for x in required_params):
        error_message = "missing required params."
        current_app.logger.debug(error_message)
        return make_response({"message": error_message}, 400)

    user_id, file_name, file_path, content_total = itemgetter(
        "user_id",
        "file_name",
        "file_path",
        "content_total",
    )(json)

    file_path = secure_filename(file_path)

    # Notify disk service
    repo = service.get_disk_repo()
    repo.create(file_name, content_total)

    # Save to database
    repo = get_files_repo()
    file_id = repo.create(file_name, user_id, file_path)

    upload_url = service.build_upload_url(file_path)

    current_app.logger.debug(
        "create_file " + str({"file_name": file_name, "file_size": content_total}),
    )
    return {"file_id": file_id, "upload_url": upload_url}


@bp.route("/<int:id>")
@permission_required("read: files")
def file_info(id):
    """ Returns the file info given a file id. """

    repo = get_files_repo()

    file_info = repo.get_by_id(id)

    if not file_info:
        return NotFound(f"File Id {id} does not exist.")

    return file_info


@bp.route("/download/<int:id>")
@permission_required("read: files")
def download(id):
    """ View for downloading a file. """

    download_url = service.get_download_url(id)

    if not download_url:
        abort(404)

    return {"download_url": download_url}


@bp.route("/delete/<int:id>", methods=["POST"])
@permission_required("write: files")
def delete(id):
    repo = get_files_repo()
    db_file = repo.get_by_id(id)

    if not db_file:
        abort(404)

    service.delete_file(id)

    return "File deleted successfully."
