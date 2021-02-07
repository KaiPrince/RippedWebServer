"""
 * Project Name: RippedWebServer
 * File Name: login_service.py
 * Programmer: Kai Prince
 * Date: Sat, Feb 06, 2021
 * Description: This file contains the login service.
"""

from auth.adapter.inbound.jwt.decode import get_payload_from_auth_token
from auth.adapter.outbound.service_api.auth import get_auth_token
from auth.adapter.outbound.session.save import clear
from auth.adapter.outbound.session.save import save_auth_ticket as persist
from auth.adapter.outbound.web.flash import flash
from auth.adapter.outbound.web.redirect import redirect_to_index
from auth.application.port.inbound.login_use_case import LoginUseCase
from auth.application.port.inbound.logout_use_case import LogoutUseCase
from auth.domain.auth_ticket import AuthTicket


class LoginController(LoginUseCase, LogoutUseCase):
    """
    * Class Name: LoginService
    * Purpose: This purpose of this class is to perform login operations.
    """

    def __init__(self, response):
        self.response = response

    def send_credentials_to_auth_service(
        self, username: str, password: str
    ) -> AuthTicket:
        auth_token = get_auth_token(username, password)
        jwt_payload = get_payload_from_auth_token(auth_token)

        return AuthTicket.from_jwt(jwt_payload)

    def clear_session(self):
        clear()

    def save_auth_ticket(self, auth_ticket: AuthTicket):
        persist(auth_ticket)

    def show_index_page(self):
        self.response.data = redirect_to_index()

    def show_login_failed_message():
        flash("Log in failed.")
