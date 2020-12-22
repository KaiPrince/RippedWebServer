import sys

from flask import (
    Blueprint, current_app, flash, g, redirect, render_template, request,
    session, url_for)
from flask.helpers import NotFound
from requests import HTTPError
from requests.exceptions import ConnectionError as r_ConnectionError
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

import common
import files.service as service
from auth.permissions import make_jwt_permissions_reader
from auth.route_decorators import login_required

# from .utils import allowed_file


bp = Blueprint("files", __name__, url_prefix="/files", template_folder="templates")


@bp.route("/")
def index():
    files = service.get_index()

    return render_template("files/index.html", files=files)


@bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    def cleanup_session():
        session.pop("file_id", None)
        current_app.logger.debug(
            "Removed File Id from session. " + str({"session": session})
        )

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

        # if allowed_file(file.filename):
        if error is not None:
            flash(error)
            return render_template("files/create.html")

        filename = secure_filename(file.filename)

        if "Content-Range" in request.headers:
            content_range, content_total = common.get_content_metadata(
                request.headers["Content-Range"]
            )
        else:
            file_size = sys.getsizeof(file)
            content_range = f"0-{file_size}"
            content_total = file_size

        try:
            return service.upload_file(
                file_name, filename, content_range, content_total, file
            )

        except (HTTPError) as e:
            current_app.logger.error(
                "POST or PUT to files service has failed. "
                + str(
                    {
                        "status_code": e.response.status_code,
                        "response": e.response.content,
                    }
                )
            )

            flash(
                f"File upload has failed. ({e.response.status_code})", category="error"
            )
            cleanup_session()
            return redirect(url_for("files.index"))
        except (
            ConnectionError,
            ConnectionAbortedError,
            r_ConnectionError,
        ) as e:
            current_app.logger.error(
                "POST or PUT to files service has failed. " + str(e)
            )

            flash("The files service could not be reached.", category="error")
            cleanup_session()
            return redirect(url_for("files.index"))
        except Exception as e:
            current_app.logger.error("Exception raised: " + str(e))

            flash("An unknown error has occured.", category="error")
            cleanup_session()
            return redirect(url_for("files.index"))

    if "file_id" in session:
        current_app.logger.debug(
            "File Id found on session. "
            + str({"file_id": session["file_id"], "session": session}),
        )

        cleanup_session()

    return render_template("files/create.html")


@bp.route("/detail/<string:id>")
@login_required
def detail(id):

    try:
        file = service.get_file(id)
    except HTTPError as e:
        message = e.response.reason
        flash(
            f"The files service was unable to serve this request. {message}",
            category="error",
        )
        return redirect(url_for("files.index"))

    # file_path = file["file_path"]
    # if file_path.endswith("txt"):
    #     content = service.get_file_content(id)
    # else:
    #     content = ""

    # NOTE: Until file_id as Hash becomes universal, we will use the file path
    #   as the id for auth.
    # TODO: Replace with hash file_id
    file_id = file["file_path"]

    permission_reader = make_jwt_permissions_reader(g.auth_token_data)
    may_delete = permission_reader.may_delete(file_id)
    may_share = permission_reader.may_share(file_id)

    return render_template(
        "files/detail.html",
        file=file,
        content="",
        may_delete=may_delete,
        may_share=may_share,
    )


@bp.route("/download/<string:id>")
@login_required
def download(id):
    """ View for downloading a file. """

    try:
        download_url = service.get_download_url(id)

    except Exception:
        flash("Failed to retrieve download url.")

        return redirect(url_for("files.index"))

    auth_token = g.auth_token

    full_url = f"{download_url}?token={auth_token}"

    return redirect(full_url)


@bp.route("/delete/<string:id>", methods=["GET", "POST"])
@login_required
def delete(id):
    file = service.get_file(id)

    if not file:
        abort(404)

    if request.method == "POST":
        try:
            service.delete_file(id)

        except (HTTPError) as e:
            current_app.logger.error(
                "DELETE to files service has failed. "
                + str(
                    {
                        "status_code": e.response.status_code,
                        "response": e.response.content,
                    }
                )
            )

            flash(f"Delete has failed. ({e.response.status_code})", category="error")
        except (
            ConnectionError,
            ConnectionAbortedError,
            r_ConnectionError,
        ) as e:
            current_app.logger.error("DELETE to files service has failed. " + str(e))

            flash("The files service could not be reached.", category="error")
        except Exception as e:
            current_app.logger.error("Exception raised: " + str(e))

            flash("An unknown error has occured.", category="error")
        finally:
            return redirect(url_for("files.index"))

    return render_template("files/delete.html", file=file)
