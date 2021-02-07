"""
 * Project Name: RippedWebServer
 * File Name: flash.py
 * Programmer: Kai Prince
 * Date: Sat, Feb 06, 2021
 * Description: This file contains functions to flash a message to the user.
"""

from flask import flash as _flash


def flash(*args, **kwargs):
    _flash(*args, **kwargs)
