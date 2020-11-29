import functools

from db.service import get_db
from flask import g, redirect, session, url_for

from .views import bp


@bp.before_app_request
def load_logged_in_user():
    user = session.get("user")

    g.user = user


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view
