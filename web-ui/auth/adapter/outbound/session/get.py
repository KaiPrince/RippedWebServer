"""
 * Project Name: RippedWebServer
 * File Name: get.py
 * Programmer: Kai Prince
 * Date: Sat, Feb 06, 2021
 * Description: This file contains functions to get from the current session.
"""

from flask import session


def get_auth_ticket():
    return session.get("auth_token_data")  # auth_ticket


def get_auth_token():
    return session.get("auth_token")
