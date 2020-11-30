import functools

from flask import g, redirect, session, url_for, request
from requests.auth import AuthBase

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
        return redirect(url_for("auth.login"))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view


class JWTAuth(AuthBase):
    """
    * Class Name: JWTAuth
    * Purpose: This purpose of this class is to inject an auth token into request
    *   headers.
    """

    def __init__(self, auth_token):
        # setup any auth-related data here
        self._auth_token = auth_token

    def __call__(self, r):
        # modify and return the request
        r.headers["Authorization"] = self._auth_token
        return r


def get_auth_middleware(auth_token: str) -> AuthBase:
    return JWTAuth(auth_token)
