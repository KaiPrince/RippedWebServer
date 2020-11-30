"""
 * Project Name: RippedWebServer
 * File Name: middleware.py
 * Programmer: Kai Prince
 * Date: Sat, Nov 28, 2020
 * Description: This file contains middleware functions for the auth module.
"""

from functools import wraps

from flask import g, redirect, session, url_for, request, abort, current_app
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
            if "Authorization" in request.headers:
                auth_token = request.headers.get("Authorization")
            elif "token" in request.query_string:
                auth_token = request.query_string["token"]
            else:
                auth_token = None

            if not auth_token:
                current_app.logger.info(
                    "Auth token missing. "
                    + str(
                        {
                            "route": request.path,
                        }
                    )
                )
                return abort(401)

            try:
                claims = service.decode_auth_token(auth_token)

                if "permissions" not in claims:
                    current_app.logger.info(
                        "Auth token is missing permissions key. "
                        + str(
                            {
                                "name": claims.get("name"),
                                "keys": claims.keys(),
                                "route": request.path,
                            }
                        )
                    )
                    return abort(401)

                permissions = claims["permissions"]
                if required_perm not in permissions:
                    current_app.logger.info(
                        "User unauthorized. "
                        + str(
                            {
                                "name": claims.get("name"),
                                "permissions": permissions,
                                "route": request.path,
                            }
                        )
                    )
                    return abort(403)
            except RuntimeError:
                current_app.logger.info(
                    "Auth token could not be decoded. "
                    + str(
                        {
                            "route": request.path,
                        }
                    )
                )
                return abort(401)

            return view(**kwargs)

        return wrapped_view

    return decorator