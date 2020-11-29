import os

import common
from db.service import get_db
from flask import Blueprint, current_app, make_response, request, send_from_directory
from flask.helpers import NotFound
from requests import HTTPError
from werkzeug.exceptions import abort

import files.service as service
from auth.middleware import permission_required

# from .utils import allowed_file


bp = Blueprint("files", __name__, url_prefix="/files", template_folder="templates")


@bp.route("/")
# @permission_required("list: files")
def index():
    db = get_db()
    files = db.execute(
        "SELECT f.id, file_name, uploaded, user_id, file_path"
        " FROM user_file f"
        " ORDER BY uploaded DESC"
    ).fetchall()

    files_array = list(dict(x) for x in files)

    for file in files_array:
        file["download_url"] = service.build_download_url(file["file_path"])
        file["upload_url"] = service.build_upload_url(file["file_path"])

    return {"files": files_array}


@bp.route("/create", methods=["POST", "PUT"])
@permission_required("write: files")
def create():
    if request.method == "POST":
        # Get params
        json = request.json

        required_params = ["user_id", "file_name", "file_path", "content_total"]
        if any(x not in json for x in required_params):
            error_message = "missing required params."
            current_app.logger.info(error_message)
            return make_response({"message": error_message}, 400)

        user_id = json["user_id"]
        file_name = json["file_name"]
        file_path = json["file_path"]
        content_total = json["content_total"]

        # Allocate in disk storage
        service.create_file(file_path, content_total)

        # Save to database
        # filename = secure_filename(file_name)
        db = get_db()
        db_cursor = db.execute(
            "INSERT INTO user_file (file_name, user_id, file_path)" " VALUES (?, ?, ?)",
            (file_name, user_id, file_path),
        )
        db.commit()

        file_id = db_cursor.lastrowid

        upload_url = service.build_upload_url(file_path)

        return {"file_id": file_id, "upload_url": upload_url}

    elif request.method == "PUT":
        # Get file path by id

        file_id = request.headers["file_id"]
        file_info = service.get_file(file_id)
        if not file_info:
            current_app.logger.debug("File id not found. " + str({"file_id": file_id}))
            return NotFound(f"File id {file_id} not found.")

        file_path = file_info["file_path"]

        # file = request.files["file"]
        content = request.data

        # TODO handle missing header
        content_range, content_total = common.get_content_metadata(
            request.headers.get("Content-Range")
        )

        # Send to disk storage service.
        try:
            file_size = service.put_file(
                file_path, content_range, content_total, content
            )

            # Do final write check
            # TODO

            return {"file_size": file_size}
        except HTTPError:
            return abort(500, "Unable to write to file.")


@bp.route("/<int:id>")
@permission_required("read: files")
def file_info(id):
    """ Returns the file info given a file id. """

    file_info = service.get_file(id)

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
    db = get_db()
    db_file = db.execute(
        "SELECT f.id, file_name as name, uploaded, user_id, file_path"
        " FROM user_file f"
        " WHERE f.id = ?"
        " ORDER BY uploaded DESC",
        [str(id)],
    ).fetchone()

    if not db_file:
        abort(404)

    service.delete_file(id)

    return "File deleted successfully."
