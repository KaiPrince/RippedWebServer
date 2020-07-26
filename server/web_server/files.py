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
)
from .db import get_db
from .auth import login_required
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
import os


ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}


bp = Blueprint("files", __name__, url_prefix="/files")


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route("/")
def index():
    db = get_db()
    files = db.execute(
        "SELECT f.id, file_name, uploaded, user_id, username"
        " FROM user_file f JOIN user u ON f.user_id = u.id"
        " ORDER BY uploaded DESC"
    ).fetchall()

    return render_template("files/index.html", files=files)


@bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
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
            flash(error)
        elif file:  # and allowed_file(file.filename):

            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))

            db = get_db()
            db.execute(
                "INSERT INTO user_file (file_name, user_id, file_path)"
                " VALUES (?, ?, ?)",
                (file_name, g.user["id"], filename),
            )
            db.commit()
            return redirect(url_for("files.index"))
    return render_template("files/create.html")


@bp.route("/detail/<int:id>")
@login_required
def detail(id):

    db = get_db()
    db_file = db.execute(
        "SELECT f.id, file_name as name, uploaded, user_id, username, file_path"
        " FROM user_file f JOIN user u ON f.user_id = u.id"
        " WHERE f.id = ?"
        " ORDER BY uploaded DESC",
        str(id),
    ).fetchone()

    if not db_file:
        abort(404)

    file = db_file

    file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], db_file["file_path"])
    with open(file_path, "rt") as f:
        content = "\n".join(f.readlines())

    return render_template("files/detail.html", file=file, content=content)


@bp.route("/download/<int:id>")
@login_required
def download(id):
    """ View for downloading a file. """

    db = get_db()
    db_file = db.execute(
        "SELECT f.id, file_name as name, uploaded, user_id, username, file_path"
        " FROM user_file f JOIN user u ON f.user_id = u.id"
        " WHERE f.id = ?"
        " ORDER BY uploaded DESC",
        str(id),
    ).fetchone()

    if "file_path" not in db_file:
        abort(404)

    file = db_file["file_path"]

    return send_from_directory(current_app.config["UPLOAD_FOLDER"], file)


@bp.route("/delete/<int:id>", methods=["GET", "POST"])
@login_required
def delete(id):
    db = get_db()
    db_file = db.execute(
        "SELECT f.id, file_name as name, uploaded, user_id, username, file_path"
        " FROM user_file f JOIN user u ON f.user_id = u.id"
        " WHERE f.id = ?"
        " ORDER BY uploaded DESC",
        str(id),
    ).fetchone()

    if not db_file:
        abort(404)

    if request.method == "POST":

        db.execute("DELETE from user_file" " WHERE id = ?", str(id))

        file_path = os.path.join(
            current_app.config["UPLOAD_FOLDER"], db_file["file_path"]
        )
        os.remove(file_path)

        db.commit()

        return redirect(url_for("files.index"))
    return render_template("files/delete.html", file=db_file)


def init_app(app):
    """ Ensure uploads folder exists. """

    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        print("Creating Upload folder at", app.config["UPLOAD_FOLDER"])
        os.mkdir(app.config["UPLOAD_FOLDER"])


def get_file(id):
    """ Consumes an ID and produces a file name. """

    db = get_db()
    db_file = db.execute(
        "SELECT f.id, file_name as name, uploaded, user_id, username, file_path"
        " FROM user_file f JOIN user u ON f.user_id = u.id"
        " WHERE f.id = ?"
        " ORDER BY uploaded DESC",
        str(id),
    ).fetchone()

    if not db_file:
        return None

    return db_file["file_path"]
