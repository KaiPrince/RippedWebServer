"""
 * Project Name: RippedWebServer
 * File Name: adapter/out/services/__init__.py
 * Programmer: Kai Prince
 * Date: Sat, Feb 06, 2021
 * Description: This file contains init functions for the outbound services
 *  module.
"""

from flask import current_app


def _base_url():
    return current_app.config["AUTH_SERVICE_URL"]
