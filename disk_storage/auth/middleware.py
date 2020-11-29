"""
 * Project Name: RippedWebServer
 * File Name: middleware.py
 * Programmer: Kai Prince
 * Date: Sat, Nov 28, 2020
 * Description: This file contains middleware functions for the auth module.
"""

from functools import wraps

from flask import g, redirect, session, url_for, request, abort
import auth.service as service

# from files.views import bp


# @bp.before_app_request
# def load_logged_in_user():
#     user = session.get("user")

#     g.user = user


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view


def permission_required(required_perm):
    def decorator(view):
        @wraps(view)
        def wrapped_view(**kwargs):
            auth_token = request.headers.get("Authorization")
            if not auth_token:
                return abort(401)

            try:
                claims = service.decode_auth_token(auth_token)
                permissions = claims.get("permissions")

                if not permissions:
                    return abort(401)

                if required_perm not in permissions:
                    return abort(403)
            except RuntimeError:
                return abort(401)

            return view(**kwargs)

        return wrapped_view

    return decorator
