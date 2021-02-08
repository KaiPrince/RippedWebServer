"""
 * Project Name: RippedWebServer
 * File Name: login_service.py
 * Programmer: Kai Prince
 * Date: Sat, Feb 06, 2021
 * Description: This file contains the login service.
"""

from auth.adapter.outbound.service_api.auth import fetch_auth_token
from auth.application.session_controller import SessionController
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
    LoginUseCase,
    LogoutUseCase,
    RefreshAuthTicketUseCase,
    BaseController,
):
    """
    * Class Name: LoginService
    * Purpose: This purpose of this class is to perform login operations.
    """

    _session_controller: SessionController

    def __init__(self, session_controller: SessionController):
        self._session_controller = session_controller

    @BaseController.new_response
    def login(self, username: str, password: str):
        try:
            super().login(username, password)

        except BadCredentialsError:
            response = flash("Invalid username or password")
            self.set_response(response)
        except RuntimeError:
            response = flash("Log in failed.")
            self.set_response(response)

    @BaseController.new_response
    def logout(self):
        # TODO: Handle exception
        return super().logout()

    @BaseController.new_response
    def refresh_auth_ticket(self):
        # TODO: Handle exception
        return super().refresh_auth_ticket()

    def _send_credentials_to_auth_service(
        self, username: str, password: str
    ) -> AuthTicket:
        auth_token = fetch_auth_token(username, password)
        return AuthTicketJwt(auth_token)

    def _clear_session(self):
        self._session_controller.clear()

    def _save_auth_ticket(self, auth_ticket: AuthTicketJwt):
        self._session_controller.save_auth_ticket(auth_ticket)

        self._session_controller.save_auth_token(auth_ticket)

        jwt_ticket = auth_ticket.to_jwt()
        user_profile = UserProfile.from_jwt(jwt_ticket)
        self._session_controller.save_user_profile(user_profile)

    @BaseController.response
    def _show_index_page(self):
        return redirect_to_index()

    @BaseController.response
    def _show_login_failed_message(self):
        return flash("Log in failed.")

    @BaseController.response
    def _show_ticket_expired_message(self):
        # current_app.logger.debug("Auth token expired " + str(token_data))

        return flash("Session expired. Please log in again.")

    @BaseController.response
    def _redirect_to_login_page(self):
        return redirect_to_login()

    def _clear_user_session_and_auth_ticket(self):
        self._session_controller.save_user_profile(None)
        self._session_controller.save_auth_token(None)
        self._session_controller.save_auth_ticket(None)

    def _user_is_logged_in(self):
        return self._session_controller.get_auth_ticket() is not None

    def _get_auth_ticket(self) -> AuthTicket:
        return self._session_controller.get_auth_ticket()
