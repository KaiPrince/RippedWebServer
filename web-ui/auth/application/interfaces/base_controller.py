"""
 * Project Name: RippedWebServer
 * File Name: base_controller.py
 * Programmer: Kai Prince
 * Date: Sun, Feb 07, 2021
 * Description: This file contains an abstract base class for controllers
 *   in the application layer.
"""

import functools
from abc import ABC
from typing import Optional

from auth.application.models.response import Response


class BaseController(ABC):
    """
    * Class Name: BaseController
    * Purpose: This purpose of this class is to define an interface for all
    *   application-level controllers.
    * NOTE: This is NOT the same as an MVC controller.
    """

    _response: Response = None

    def set_response(self, response: Response):
        self._response = response

    def clear_response(self):
        self._response = None

    def has_response(self) -> bool:
        return self._response is not None

    def get_response(self) -> Response:
        if self._response is None:
            raise ValueError("Response has not been set.")
        return self._response

    def get_response_or_none(self) -> Optional[Response]:
        return self._response

    def new_response(self, func):
        """ Reset the controller for a new response. """

        @functools.wraps(func)
        def wrapped_func(**kwargs):
            self.set_response(None)

            return func(**kwargs)

        return wrapped_func
