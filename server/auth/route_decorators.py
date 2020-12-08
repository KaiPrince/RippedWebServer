import functools

from flask import current_app, flash, g, redirect, session, url_for, request
import auth.service as service
from datetime import timedelta, datetime


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if request.args.get("token"):
            auth_token = request.args.get("token")
            payload = service.get_payload_from_auth_token(auth_token)

            if service.is_token_expired(payload):
                flash("This token has expired. Please request another.", "error")
                return redirect(url_for("index"))

            g.auth_token = auth_token
            g.auth_token_data = payload

            message = "You are being granted temporary access"

            if "exp" in payload:
                expiry_time = datetime.fromtimestamp(payload["exp"])
                distance = expiry_time - datetime.now()
                days = distance.days
                hours = round(distance.seconds / 60 / 60)
                minutes = round((distance.seconds % 3600) / 60)

                message += ", which will expire in "
                message += f"{days} days, {hours} hours, {minutes} minutes"

            message += "."

            flash(message, "warning")

        elif g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view
