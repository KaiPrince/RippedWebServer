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
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
from db.service import get_db
from .service import delete_file

# from .utils import allowed_file


bp = Blueprint("files", __name__, url_prefix="/files", template_folder="templates")


@bp.route("/")
def index():
    db = get_db()
    files = db.execute(
        "SELECT f.id, file_name, uploaded, user_id, username, file_path"
        " FROM user_file f JOIN user u ON f.user_id = u.id"
        " ORDER BY uploaded DESC"
    ).fetchall()

    return render_template("files/index.html", files=files)


@bp.route("/create", methods=["GET", "POST"])
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

    content = ""
    if file_path.endswith("txt"):
        with open(file_path, "rt") as f:
            content = "\n".join(f.readlines())

    return render_template("files/detail.html", file=file, content=content)


@bp.route("/download/<int:id>")
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

    if db_file is None or "file_path" not in db_file.keys():
        abort(404)

    file = db_file["file_path"]

    file_dir = os.path.abspath(current_app.config["UPLOAD_FOLDER"])

    return send_from_directory(file_dir, file, as_attachment=True)


@bp.route("/delete/<int:id>", methods=["GET", "POST"])
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

        delete_file(id)

        return redirect(url_for("files.index"))
    return render_template("files/delete.html", file=db_file)
