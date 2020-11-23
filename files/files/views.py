import os
from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
    current_app,
    send_from_directory,
    make_response,
)
from flask.helpers import NotFound
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
from db.service import get_db
import files.service as service
import common

# from .utils import allowed_file


bp = Blueprint("files", __name__, url_prefix="/files", template_folder="templates")


@bp.route("/")
def index():
    db = get_db()
    files = db.execute(
        "SELECT f.id, file_name, uploaded, user_id, file_path"
        " FROM user_file f"
        " ORDER BY uploaded DESC"
    ).fetchall()

    files_array = list(dict(x) for x in files)

    return {"files": files_array}


@bp.route("/create", methods=["POST", "PUT"])
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
        service.create_file(file_name, content_total)

        # Save to database
        filename = secure_filename(file_name)
        db = get_db()
        db_cursor = db.execute(
            "INSERT INTO user_file (file_name, user_id, file_path)" " VALUES (?, ?, ?)",
            (file_name, user_id, filename),
        )
        db.commit()

        file_id = db_cursor.lastrowid

        return {"file_id": file_id}

    elif request.method == "PUT":
        # Get file path by id
        file_id = request.headers["file_id"]
        file_path = service.get_file(file_id)["file_path"]

        # file = request.files["file"]
        content = request.data

        # TODO handle missing header
        content_range, content_total = common.get_content_metadata(
            request.headers.get("Content-Range")
        )

        # Send to disk storage service.
        service.put_file(file_path, content_range, content_total, content)
        file_size = 100

        # Do final write check
        # TODO

        return {"file_size": file_size}


@bp.route("/<int:id>")
def file_info(id):
    """ Returns the file info given a file id. """

    file_info = service.get_file(id)

    if not file_info:
        return NotFound(f"File Id {id} does not exist.")

    return file_info


@bp.route("/content/<int:id>")
def file_content(id):
    """ Returns the file content given a file id. """

    return service.get_file_content(id)


@bp.route("/detail/<int:id>")
def detail(id):

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

    file = dict(db_file)

    file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], db_file["file_path"])

    content = ""
    if file_path.endswith("txt"):
        with open(file_path, "rt") as f:
            content = "\n".join(f.readlines())

    return {"file": file, "content": content}


@bp.route("/download/<int:id>")
def download(id):
    """ View for downloading a file. """

    db = get_db()
    db_file = db.execute(
        "SELECT f.id, file_name as name, uploaded, user_id, username, file_path"
        " FROM user_file f"
        " WHERE f.id = ?"
        " ORDER BY uploaded DESC",
        [str(id)],
    ).fetchone()

    if db_file is None or "file_path" not in db_file.keys():
        abort(404)

    file = db_file["file_path"]

    file_dir = os.path.abspath(current_app.config["UPLOAD_FOLDER"])

    return send_from_directory(file_dir, file, as_attachment=True)


@bp.route("/delete/<int:id>", methods=["POST"])
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
