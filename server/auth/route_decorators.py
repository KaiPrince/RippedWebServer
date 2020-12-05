import functools

from flask import current_app, flash, g, redirect, session, url_for, request
import auth.service as service


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if request.args.get("token"):
            auth_token = request.args.get("token")
            payload = service.get_payload_from_auth_token(auth_token)

            g.auth_token = auth_token
            g.auth_token_data = payload

            flash("You are being granted temporary access")

        elif g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view
