from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
    make_response,
)
import auth.service as service

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

    error = None
    user = service.find_user(username)

    if user is None:
        error = "Incorrect username."
    elif not service.does_password_match(password, user["password"]):
        error = "Incorrect password."

    if error is None:
        return {
            "user_id": user["id"],
            "permissions": service.get_user_permissions(user["id"]),
        }

    return make_response(error, 400)


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))
