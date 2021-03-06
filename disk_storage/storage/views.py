import os

from flask import (Blueprint, Response, abort, current_app, request,
                   send_from_directory, url_for)
from flask.helpers import BadRequest, NotFound
from flask_cors import cross_origin

import common
# from werkzeug.exceptions import abort
import storage.service as service
from auth.middleware import permission_required

# from http import HTTPStatus


# from .utils import allowed_file


bp = Blueprint("storage", __name__, url_prefix="/storage")


@bp.route("/")
@permission_required("read: disk_storage")
def index():

    files = service.list_files()

    return {"files": files}


@bp.route("/create", methods=["POST"])
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
        "file_path": file_name_on_disk,
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


@bp.route("/download/<path:file_name>")
@permission_required("read: disk_storage")
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


@bp.route("/speedtest")
@cross_origin()
def speedtest():
    """ This view handler streams random data to the requester. """

    # TODO rate limit

    def generate():
        size_in_bytes = 1 * 1000 * 1000  # 1MB
        chunk_size = 200
        for x in range(0, size_in_bytes, chunk_size):
            yield os.urandom(chunk_size)

    return Response(generate())
