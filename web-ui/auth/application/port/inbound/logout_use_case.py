"""
 * Project Name: RippedWebServer
 * File Name: logout_use_case.py
 * Programmer: Kai Prince
 * Date: Sat, Feb 06, 2021
 * Description: This file contains the log out use case.
"""

from abc import ABC, abstractmethod


class LogoutUseCase(ABC):
    """
    * Class Name: LogoutUseCase
    * Purpose: This purpose of this class is to define the log out user story.

    * Given: The user is currently logged it,
    * When: the user logs out,
    * Then: the user's session and Auth Ticket are cleared from memory,
    *   and the user is redirected to the home page.
    """

    def logout(self):
        if self._user_is_logged_in():
            self._clear_user_session_and_auth_ticket()
            self._show_index_page()

    @abstractmethod
    def _user_is_logged_in(self):
        pass

    @abstractmethod
    def _clear_user_session_and_auth_ticket(self):
        pass

    @abstractmethod
    def _show_index_page(self):
        pass
