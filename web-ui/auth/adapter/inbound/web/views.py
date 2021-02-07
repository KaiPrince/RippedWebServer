from flask import (
    Blueprint,
    current_app,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

import auth.service as service
import files.service as files_service
from auth.adapter.inbound.web.route_decorators import login_required

from auth.application.login_controller import LoginController

bp = Blueprint("auth", __name__, url_prefix="/auth", template_folder="templates")


@bp.before_app_request
def load_logged_in_user():
    user = session.get("user")

    g.user = user


@bp.before_app_request
def load_auth_token():
    g.auth_token = session.get("auth_token")
    g.auth_token_data = session.get("auth_token_data")


@bp.before_app_request
def refresh_auth_token():
    token_data = session.get("auth_token_data")

    if token_data is not None and is_token_expired(token_data):
        session.clear()
        flash("Session expired. Please log in again.")

        current_app.logger.debug("Auth token expired " + str(token_data))
        return redirect(url_for("auth.login"))


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error = None

        # TEMP disable adding new users TODO: Remove.
        error = "User registration is disabled."

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

        response = object()
        login_controller = LoginController(response)
        login_controller.login(username, password)

        return response.data

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@bp.route("/generate_sharing_link")
@login_required
def generate_sharing_link():
    duration = request.args.get("duration")
    file_id = request.args.get("file_id")

    file_path = files_service.get_file(file_id)["file_path"]

    permissions_needed = ["read: files", "read: disk_storage"]
    share_token = service.request_share_token(
        g.auth_token,
        file_path,
        duration,
        permissions_needed,
    )

    public_url = current_app.config["PUBLIC_FILES_SERVICE_URL"]
    share_link = public_url + url_for("files.detail", id=file_id, token=share_token)

    return {"link": share_link}
