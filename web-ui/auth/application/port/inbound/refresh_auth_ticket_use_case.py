"""
 * Project Name: RippedWebServer
 * File Name: refresh_auth_ticket_use_case.py
 * Programmer: Kai Prince
 * Date: Sun, Feb 07, 2021
 * Description: This file contains the refresh auth ticket use case.
"""

from abc import ABC, abstractmethod
from auth.domain.auth_ticket import AuthTicket


class RefreshAuthTicketUseCase(ABC):
    """
    * Class Name: RefreshAuthTicketUseCase
    * Purpose: This purpose of this class is to define the refresh auth
    *   ticket use case.
    *
    * As: a user,
    * Given: An auth ticket,
    * When: I visit a page,
    * If: the ticket has expired,
    * Then: I am shown an error message,
    *   and my session is cleared,
    *   and redirected to the log in page.
    """

    def refresh_auth_ticket(self):
        auth_ticket: AuthTicket = self._get_auth_ticket()

        if auth_ticket is not None and auth_ticket.is_expired():
            self._show_ticket_expired_message()
            self._clear_session()
            self._redirect_to_login_page()

    @abstractmethod
    def _show_ticket_expired_message(self):
        pass

    @abstractmethod
    def _clear_session(self):
        pass

    @abstractmethod
    def _redirect_to_login_page(self):
        pass

    @abstractmethod
    def _get_auth_ticket(self) -> AuthTicket:
        pass
