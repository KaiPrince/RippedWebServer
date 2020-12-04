from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
    make_response,
    current_app,
)
import auth.service as service
from authlib.jose import jwt
from datetime import timedelta
from time import time
from operator import itemgetter

bp = Blueprint("auth", __name__, url_prefix="/auth", template_folder="templates")


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        # TEMP disable adding new users TODO: Remove.
        # error = "User registration is disabled."

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif (
            db.execute("SELECT id FROM user WHERE username = ?", (username,)).fetchone()
            is not None
        ):
            error = "User {} is already registered.".format(username)

        if error is None:
            create_user(username, password)
            return redirect(url_for("auth.login"))

        make_response(error, 400)

    return render_template("auth/register.html")


@bp.route("/login", methods=["POST"])
def login():
    username = request.json["username"]
    password = request.json["password"]

    user = service.find_user(username)

    successful_login = user is not None and service.does_password_match(
        password, user["password"]
    )

    if successful_login:
        header = {"alg": "HS256"}

        payload = {
            "sub": user["id"],
            "name": user["username"],
            "permissions": service.get_user_permissions(user["id"]),
            "iat": int(time()),
            "exp": int(time()) + timedelta(hours=1).total_seconds(),
        }

        key = current_app.config["JWT_KEY"]
        token = jwt.encode(header, payload, key).decode("utf-8")

        current_app.logger.info(
            "User successfully logged in. " + str({"username": username})
        )

        return {"JWT": token}

    current_app.logger.info("User failed to log in. " + str({"username": username}))

    return make_response("Incorrect username or password.", 400)


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@bp.route("/request_share_token", methods=["POST"])
def request_share_token():
    """Consumes an user-based auth token and token details,
    and produces a resource-based auth token."""

    user_token = request.headers.get("Authorization")

    if not user_token:
        return make_response("Auth token missing", 401)

    requester, file_path, duration, requested_permissions, = itemgetter(
        "requester",
        "file_path",
        "duration",
        "permissions",
    )(request.json)

    try:
        user_token_payload = service.get_token_payload(user_token)
    except Exception:
        return make_response("Invalid auth token.", 400)

    if not service.validate_share_token_request(
        user_token_payload, requester, requested_permissions
    ):
        return make_response("Request not valid.", 403)

    resource_token = service.generate_resource_token(
        requester, file_path, duration, requested_permissions
    )

    return {"token": resource_token}
