from flask import current_app, flash, g, redirect, session, url_for

from auth.application.login_controller import LoginController
from .views import bp

from auth.adapter.outbound.session.get import get_auth_ticket
from auth.domain.auth_ticket import AuthTicket


@bp.before_app_request
def make_app_controllers():
    login_controller = LoginController()

    g.login_controller = login_controller


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
    auth_ticket = get_auth_ticket()

    if auth_ticket is not None:
        auth_ticket = AuthTicket.from_jwt(auth_ticket)

        login_controller: LoginController = g.login_controller
        login_controller.refresh_auth_ticket(auth_ticket)

        return login_controller.get_response_or_none()


