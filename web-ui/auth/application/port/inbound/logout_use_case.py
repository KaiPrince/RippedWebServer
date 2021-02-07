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
    * Then: the user's session and Auth Token are cleared from memory.
    """

    @abstractmethod
    def logout(self):
        if self.user_is_logged_in():
            self.clear_user_session_and_auth_token()
