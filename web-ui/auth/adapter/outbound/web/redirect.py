"""
 * Project Name: RippedWebServer
 * File Name: redirect.py
 * Programmer: Kai Prince
 * Date: Sat, Feb 06, 2021
 * Description: This file contains functions to redirect the view.
"""

from flask import redirect, url_for


def redirect_to_index():
    return redirect(url_for("index"))
