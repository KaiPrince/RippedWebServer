"""
 * Project Name: RippedWebServer
 * File Name: session.py
 * Programmer: Kai Prince
 * Date: Sat, Feb 06, 2021
 * Description: This file contains functions to get from and save to the current session.
"""

from flask import session as _session
from auth.application.port.outbound.session import Session


class FlaskSession(Session):

    def get(self, key: str) -> object:
        return _session.get(key)

    def set(self, key: str, data: object) -> None:
        _session[key] = data

    def clear(self) -> None:
        _session.clear()
