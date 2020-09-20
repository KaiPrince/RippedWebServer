import os
from flask import (
    Blueprint,
    request,
    current_app,
    send_from_directory,
)
from flask.helpers import BadRequest, NotFound

# from http import HTTPStatus

# from werkzeug.exceptions import abort
from .service import list_files, get_file, create_file, delete_file

# from .utils import allowed_file


bp = Blueprint("storage", __name__, url_prefix="/storage")


@bp.route("/")
def index():

    files = list_files()

    return {"files": files}


@bp.route("/create", methods=["POST"])
def create():
    file_name = request.form["file_name"]
    file = request.files["file"]
    error = None

    if not file_name:
        error = "File name is required."

    # check if the post request has the file part
    if "file" not in request.files:
        error = "No file part"

    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == "":
        error = "No selected file"

    if error is not None:
        return BadRequest(error)

    response = create_file(file_name, file)
    return {"file_name": response}


@bp.route("/detail", methods=["POST"])
def detail():

    file_name = request.form["file_name"]

    file_path = current_app.config["UPLOAD_FOLDER"]

    contents = get_file(os.path.join(file_path, file_name))

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
    "/delete/<path:file_name>",
    methods=["POST"],
)
def delete(file_name):

    # file_name = request.form["file_name"]

    # if not db_file:
    #     abort(404)

    try:
        delete_file(file_name)
    except FileNotFoundError:
        return NotFound(file_name)

    return ""
