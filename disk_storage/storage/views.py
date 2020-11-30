import os

import common

# from werkzeug.exceptions import abort
import storage.service as service
from flask import (
    Blueprint,
    current_app,
    request,
    send_from_directory,
    url_for,
    abort,
    safe_join,
    render_template,
)
from flask.helpers import BadRequest, NotFound

from auth.middleware import permission_required
from storage.sockets import socket_io

# from http import HTTPStatus


# from .utils import allowed_file


bp = Blueprint("storage", __name__, url_prefix="/storage", template_folder="templates")


@bp.route("/")
@permission_required("read: disk_storage")
def index():

    files = service.list_files()

    return {"files": files}


@bp.route("/create/", methods=["POST"])
@permission_required("write: disk_storage")
def create():
    # Get params
    json = request.json

    required_params = ["file_path", "content_total"]
    if any(x not in json for x in required_params):
        error_message = "missing required params."
        current_app.logger.info(error_message)
        return BadRequest(error_message)

    file_path = request.json["file_path"]
    file_size = request.json["content_total"]

    file_name_on_disk = service.create_file(file_path, file_size)
    if not file_name_on_disk:
        return abort(507)

    return {
        "file_name": file_name_on_disk,
        "upload_url": url_for("storage.write", file_path=file_path),
    }


@bp.route("/create/<path:file_path>", methods=["PUT"])
@permission_required("write: disk_storage")
def write(file_path):

    # TODO handle missing header
    content_range, content_total = common.get_content_metadata(
        request.headers.get("Content-Range")
    )

    if file_path is None:
        return NotFound("File path required.")

    # file: FileStorage = request.files["file"]
    # TODO add buffer to protect memory
    # content = file.stream.read()
    content = request.data

    insert_position = int(content_range.split("-")[0])

    file_size = service.put_file(file_path, insert_position, content)
    return {"file_size": file_size}


@bp.route("/download-small/<path:file_name>")
# @permission_required("read: disk_storage")
def download(file_name):
    """ View for downloading a file. """

    # if db_file is None or "file_path" not in db_file.keys():
    #     abort(404)

    file_dir = os.path.abspath(current_app.config["UPLOAD_FOLDER"])

    return send_from_directory(file_dir, file_name, as_attachment=True)


@bp.route("/delete/<path:file_name>", methods=["POST"])
@permission_required("write: disk_storage")
def delete(file_name):

    try:
        service.delete_file(file_name)
    except FileNotFoundError:
        return NotFound(f"File {file_name} was not found.")

    return f"File {file_name} was deleted."


@bp.route("/download/<path:file_name>")
# @permission_required("read: disk_storage")
def download_stream(file_name):
    """ View for downloading a file. """

    # if db_file is None or "file_path" not in db_file.keys():
    #     abort(404)

    file_dir = current_app.config["UPLOAD_FOLDER"]

    file_path = safe_join(file_dir, file_name)

    @socket_io.on("connect")
    def connect():
        service.pass_in_chunks(
            file_path, lambda content: socket_io.emit("data", content)
        )

        socket_io.emit("done")

    return render_template("download.html", file_path=file_path, file_name=file_name)
