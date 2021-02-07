"""
 * Project Name: RippedWebServer
 * File Name: save.py
 * Programmer: Kai Prince
 * Date: Sat, Feb 06, 2021
 * Description: This file contains functions to save to the session.
"""

from flask import session


def clear():
    session.clear()


def save_auth_ticket(auth_ticket: dict):
    session["auth_token_data"] = auth_ticket  # auth_ticket


def save_auth_token(auth_token: str):
    session["auth_token"] = auth_token


def save_user_profile(user_profile: dict):
    session["user"] = user_profile
