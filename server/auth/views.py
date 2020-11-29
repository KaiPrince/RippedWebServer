from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
    current_app,
)
import auth.service as service
from requests.exceptions import HTTPError

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
            user = service.get_user_data_from_auth_token(auth_token)

            session.clear()

            session["user"] = {"username": user["name"], "id": user["sub"]}
            session["auth_token"] = auth_token

            current_app.logger.debug(
                "Log in successful. "
                + str(
                    {
                        "username": user["name"],
                        "id": user["sub"],
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
