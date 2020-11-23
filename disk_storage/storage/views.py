import os

import common
# from werkzeug.exceptions import abort
import storage.service as service
from flask import Blueprint, current_app, request, send_from_directory
from flask.helpers import BadRequest, NotFound

# from http import HTTPStatus


# from .utils import allowed_file


bp = Blueprint("storage", __name__, url_prefix="/storage")


@bp.route("/")
def index():

    files = service.list_files()

    return {"files": files}


@bp.route("/create", methods=["POST", "PUT"])
def create():
    if request.method == "POST":
        # Get params
        json = request.json

        required_params = ["file_path", "content_total"]
        if any(x not in json for x in required_params):
            error_message = "missing required params."
            current_app.logger.info(error_message)
            return BadRequest(error_message)

        file_path = request.json["file_path"]
        content_total = request.json["content_total"]

        response = service.create_file(file_path)
        return {"file_name": response}

    elif request.method == "PUT":
        # TODO handle missing header
        content_range, content_total = common.get_content_metadata(
            request.headers.get("Content-Range")
        )
        file_path = request.headers["file_path"]

        # file: FileStorage = request.files["file"]
        # TODO add buffer to protect memory
        # content = file.stream.read()
        content = request.data

        insert_position = int(content_range.split("-")[0])

        file_size = service.put_file(file_path, insert_position, content)
        return {"file_size": file_size}


@bp.route("/file-content")
def detail():

    file_name = request.headers["file_path"]

    file_path = current_app.config["UPLOAD_FOLDER"]

    contents = service.get_file(os.path.join(file_path, file_name))

    # if not db_file:
    #     abort(404)

    # file_path = os.path.join(current_app.config["UPLOAD_FOLDER"],
    # db_file["file_path"])

    # content = ""
    # if file_path.endswith("txt"):
    #     with open(file_path, "rt") as f:
    #         content = "\n".join(f.readlines())

    return contents


@bp.route("/download/<path:file_name>")
def download(file_name):
    """ View for downloading a file. """

    # if db_file is None or "file_path" not in db_file.keys():
    #     abort(404)

    file_dir = os.path.abspath(current_app.config["UPLOAD_FOLDER"])

    return send_from_directory(file_dir, file_name, as_attachment=True)


@bp.route(
    "/delete",  # /<path:file_name>",
    methods=["POST"],
)
def delete():  # file_name):

    file_name = request.headers["file_path"]

    try:
        service.delete_file(file_name)
    except FileNotFoundError:
        return NotFound(f"File {file_name} was not found.")

    return f"File {file_name} was deleted."
