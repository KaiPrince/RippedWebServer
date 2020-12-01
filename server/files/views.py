import sys
from io import BytesIO

from flask import (Blueprint, Response, current_app, flash, g, redirect,
                   render_template, request, send_file, session, url_for)
from flask.helpers import NotFound
from requests import HTTPError
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

import common
import files.service as service
from auth.middleware import login_required

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

            if "Content-Range" in request.headers:
                content_range, content_total = common.get_content_metadata(
                    request.headers["Content-Range"]
                )
            else:
                file_size = sys.getsizeof(file)
                content_range = f"0-{file_size}"
                content_total = file_size

            if "file_id" not in session:
                current_app.logger.debug(
                    "File Id not found on session. This must be the first packet."
                )
                # ..Send create request on first packet.
                # TODO pass total size and check free disk space
                file_id = service.create_file(
                    file_name, g.user["id"], filename, content_total
                )

                if not file_id:
                    abort(500, "Couldn't create new file.")

                session["file_id"] = file_id
            else:
                current_app.logger.debug(
                    "File Id found on session. "
                    + str({"file_id": session["file_id"], "session": session}),
                )
                file_id = session["file_id"]

            try:
                service.put_file(file_id, content_range, content_total, file)

                # Clean session
                content_range_end = int(content_range.split("-")[-1])
                if content_range_end >= int(content_total) - 1:
                    current_app.logger.debug("Final packet recieved.")
                    session.pop("file_id", None)
                    current_app.logger.debug(
                        "Removed File Id from session. " + str({"session": session})
                    )

                    return redirect(url_for("files.index"))

            except HTTPError as e:
                current_app.logger.warn(
                    "PUT file to files service has failed. "
                    + str(
                        {
                            "status_code": e.response.status_code,
                            "response": e.response.content,
                        }
                    )
                )
                flash("File upload failed.")
                session.pop("file_id", None)
                current_app.logger.debug(
                    "Removed File Id from session. " + str({"session": session})
                )

                return redirect(url_for("files.index"))
            except Exception as e:
                session.pop("file_id", None)
                current_app.logger.debug(
                    "Removed File Id from session. " + str({"session": session})
                )
                raise e

            return {"files": [{"name": file_name}]}

    if "file_id" in session:
        current_app.logger.debug(
            "File Id found on session. "
            + str({"file_id": session["file_id"], "session": session}),
        )

        session.pop("file_id", None)
        current_app.logger.debug(
            "Removed File Id from session. " + str({"session": session})
        )

    return render_template("files/create.html")


@bp.route("/detail/<int:id>")
@login_required
def detail(id):

    try:
        file = service.get_file(id)
    except HTTPError as e:
        message = e.response.reason
        return NotFound(message)

    # file_path = file["file_path"]
    # if file_path.endswith("txt"):
    #     content = service.get_file_content(id)
    # else:
    #     content = ""

    return render_template("files/detail.html", file=file, content="")


@bp.route("/download/<int:id>")
@login_required
def download(id):
    """ View for downloading a file. """

    download_url = service.get_download_url(id)

    auth_token = g.auth_token

    full_url = f"{download_url}?token={auth_token}"

    return redirect(full_url)


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
