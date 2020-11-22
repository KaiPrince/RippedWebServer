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
from auth.middleware import login_required
import files.service as service

# from .utils import allowed_file


bp = Blueprint("files", __name__, url_prefix="/files", template_folder="templates")


@bp.route("/")
def index():
    files = service.get_index()

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

            service.create_file(file_name, g.user["id"], filename)

            return redirect(url_for("files.index"))
    return render_template("files/create.html")


@bp.route("/detail/<int:id>")
@login_required
def detail(id):

    file = service.get_file(id)
    content = service.get_file_content(id)

    return render_template("files/detail.html", file=file, content=content)


@bp.route("/download/<int:id>")
@login_required
def download(id):
    """ View for downloading a file. """

    return service.download_file(id)


@bp.route("/delete/<int:id>", methods=["GET", "POST"])
@login_required
def delete(id):
    file = service.get_file(id)

    if not file:
        abort(404)

    if request.method == "POST":

        service.delete_file(id)

        return redirect(url_for("files.index"))
    return render_template("files/delete.html", file=file)
