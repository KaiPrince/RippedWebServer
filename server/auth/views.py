from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
    g,
)
from requests.exceptions import HTTPError

import auth.service as service
import files.service as files_service

bp = Blueprint("auth", __name__, url_prefix="/auth", template_folder="templates")


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error = None

        # TEMP disable adding new users TODO: Remove.
        # error = "User registration is disabled."

        # TODO

        if error is None:
            # create_user(username, password)
            return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        try:
            auth_token = service.get_auth_token(username, password)
            payload = service.get_payload_from_auth_token(auth_token)

            session.clear()

            session["user"] = {"username": payload["name"], "id": payload["sub"]}
            session["auth_token"] = auth_token
            session["auth_token_data"] = payload

            current_app.logger.debug(
                "Log in successful. "
                + str(
                    {
                        "username": payload["name"],
                        "id": payload["sub"],
                        "auth_token": auth_token,
                    }
                )
            )
            return redirect(url_for("index"))

        except HTTPError as e:
            current_app.logger.debug(
                "Log in failed. " + str({"status_code": e.response.status_code})
            )
            flash("Log in failed.")

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@bp.route("/generate_sharing_link")
def generate_sharing_link():
    duration = request.args.get("duration")
    file_id = request.args.get("file_id")

    file_path = files_service.get_file(file_id)["file_path"]

    permissions_needed = ["read: disk_storage"]
    share_token = service.request_share_token(
        g.auth_token,
        file_path,
        duration,
        permissions_needed,
    )

    download_url = files_service.get_download_url(id)

    share_link = download_url + "?token=" + share_token

    return {"link": share_link}
