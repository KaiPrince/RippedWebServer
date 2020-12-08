from flask import current_app, flash, g, redirect, session, url_for

from .views import bp
from .service import is_token_expired


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
