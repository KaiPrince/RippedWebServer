"""
 * Project Name: RippedWebServer
 * File Name: login_service.py
 * Programmer: Kai Prince
 * Date: Sat, Feb 06, 2021
 * Description: This file contains the login service.
"""

from auth.adapter.outbound.service_api.auth import fetch_auth_token
from auth.adapter.outbound.session.save import (
    clear,
    save_auth_ticket as _save_auth_ticket,
    save_user_profile,
    save_auth_token,
)
from auth.adapter.outbound.session.get import get_auth_token
from auth.adapter.outbound.web.flash import flash
from auth.adapter.outbound.web.redirect import redirect_to_index, redirect_to_login
from auth.application.exceptions.bad_credentials import BadCredentialsError
from auth.application.models.auth_ticket_jwt import AuthTicketJwt
from auth.application.port.inbound.login_use_case import LoginUseCase
from auth.application.port.inbound.logout_use_case import LogoutUseCase
from auth.application.port.inbound.refresh_auth_ticket_use_case import (
    RefreshAuthTicketUseCase,
)
from auth.domain.auth_ticket import AuthTicket
from auth.application.interfaces.base_controller import BaseController
from auth.domain.user_profile import UserProfile


class LoginController(
    BaseController,
    LoginUseCase,
    LogoutUseCase,
    RefreshAuthTicketUseCase,
):
    """
    * Class Name: LoginService
    * Purpose: This purpose of this class is to perform login operations.
    """

    def __init__(self):
        pass

    def login(self, username: str, password: str):
        self.clear_response()

        try:
            super().login(username, password)
        except BadCredentialsError:
            response = flash("Invalid username or password")
            self.set_response(response)
        except RuntimeError:
            response = flash("Log in failed.")
            self.set_response(response)

    def logout(self):
        # TODO: Handle exception
        return super().logout()

    def refresh_auth_ticket(self, auth_ticket: AuthTicket):
        return super().refresh_auth_ticket(auth_ticket)

    # TODO: hide non-usecase entry methods

    def send_credentials_to_auth_service(
        self, username: str, password: str
    ) -> AuthTicket:
        auth_token = fetch_auth_token(username, password)
        # jwt_payload = get_payload_from_auth_token(auth_token)
        # return AuthTicket.from_jwt(jwt_payload)
        return AuthTicketJwt(auth_token)

    def clear_session(self):
        clear()

    def save_auth_ticket(self, auth_ticket: AuthTicketJwt):
        jwt_ticket = auth_ticket.to_jwt()
        _save_auth_ticket(jwt_ticket)

        auth_token = auth_ticket.get_encoded_jwt()
        save_auth_token(auth_token)

        user_profile = UserProfile.from_jwt(jwt_ticket)
        save_user_profile(user_profile.to_dict())

    def show_index_page(self):
        self.set_response(redirect_to_index())

    def show_login_failed_message(self):
        self.set_response(flash("Log in failed."))

    def show_ticket_expired_message(self):
        # current_app.logger.debug("Auth token expired " + str(token_data))

        self.set_response(flash("Session expired. Please log in again."))

    def redirect_to_login_page(self):
        self.set_response(redirect_to_login())

    def clear_user_session_and_auth_ticket(self):
        # TODO adjust type hinting, add documentation?
        save_user_profile(None)
        save_auth_token(None)
        _save_auth_ticket(None)

    def user_is_logged_in(self):
        return get_auth_token() is not None
