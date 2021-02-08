from flask import g

from auth.application.login_controller import LoginController
from auth.application.session_controller import SessionController
from .views import bp
from ...outbound.session import FlaskSession


@bp.before_app_request
def make_app_controllers():
    g.session_controller = SessionController(FlaskSession())
    g.login_controller = LoginController(g.session_controller)


@bp.before_app_request
def load_logged_in_user():
    user_profile = g.session_controller.get_user_profile()
    g.user = user_profile.to_dict() if user_profile else None


@bp.before_app_request
def load_auth_token():
    auth_token = g.session_controller.get_auth_token()
    g.auth_token = auth_token.get_encoded_jwt() if auth_token else None

    auth_token_data = g.session_controller.get_auth_ticket()
    g.auth_token_data = auth_token_data.to_jwt() if auth_token_data else None


@bp.before_app_request
def refresh_auth_token():
    login_controller: LoginController = g.login_controller
    login_controller.refresh_auth_ticket()

    return login_controller.get_response_or_none()
