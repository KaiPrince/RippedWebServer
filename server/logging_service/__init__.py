"""
 * Project Name: RippedWebServer
 * File Name: __init__.py
 * Programmer: Kai Prince
 * Date: Tue, Dec 01, 2020
 * Description: This file contains the logging app.
"""
from flask import Flask
from .logger import make_log_handler


def init_app(app: Flask, app_name):
    # set up logging
    log_handler = make_log_handler(
        app.config["LOGGING_SERVICE_URL"],
        app.config["LOGGING_AUTH_TOKEN"],
        app_name,
    )
    app.logger.addHandler(log_handler)
