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

import auth.application.port.outbound.auth as service
import files.service as files_service
from auth.adapter.inbound.web.route_decorators import login_required

from auth.application.login_controller import LoginController
from auth.adapter.inbound.session.get import get_auth_ticket
from auth.domain.auth_ticket import AuthTicket

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
    auth_ticket = get_auth_ticket()

    if auth_ticket is not None:
        auth_ticket = AuthTicket.from_jwt(auth_ticket)

        # TODO move to factory or context global
        login_controller = LoginController()
        login_controller.refresh_auth_ticket(auth_ticket)

        return login_controller.get_response()


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

        login_controller = LoginController()
        login_controller.login(username, password)

        return login_controller.get_response()

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
