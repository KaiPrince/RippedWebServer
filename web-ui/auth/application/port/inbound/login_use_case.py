"""
 * Project Name: RippedWebServer
 * File Name: login_use_case.py
 * Programmer: Kai Prince
 * Date: Sat, Feb 06, 2021
 * Description: This file contains the Login Use Case.
"""

from abc import ABC, abstractmethod
from auth.domain.auth_ticket import AuthTicket


class LoginUseCase(ABC):
    """
    * Class Name: LoginUseCase
    * Purpose: This purpose of this class is to define the user story
    *  of the log in process.

    * Given: A username and password,
    * When: a log in request is submitted,
    * Then: the credentials are sent to the Auth service,
    *   and if an Auth Token is returned,
    *   then the session is cleared,
    *   and the Auth Token is retained,
    *   and the user is redirected to the index page,
    *   otherwise an error message is shown.
    """

    def login(self, username: str, password: str):
        auth_ticket = self._send_credentials_to_auth_service(username, password)

        if auth_ticket:
            self._clear_session()
            self._save_auth_ticket(auth_ticket)
            self._show_index_page()
        else:
            self._show_login_failed_message()

    @abstractmethod
    def _send_credentials_to_auth_service(
        self, username: str, password: str
    ) -> AuthTicket:
        pass

    @abstractmethod
    def _clear_session(self):
        pass

    @abstractmethod
    def _save_auth_ticket(self, auth_ticket: AuthTicket):
        pass

    @abstractmethod
    def _show_index_page(self):
        pass

    @abstractmethod
    def _show_login_failed_message(self):
        pass
