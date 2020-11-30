"""
* Project Name: RippedWebServer
* File Name: __init__.py
* Programmer: Kai Prince
* Date: Sun, Jul 19, 2020
* Description: This file contains the main entry point for the app.
"""

import os

import auth.views
import db
from flask import Flask

import auth

from .config import getConfig


def create_app(test_config=None):
    # create and configure the app
    app = Flask(
        __name__,
        instance_relative_config=True,
    )

    # TODO: collapse with below
    app_config = getConfig(app)
    app.config.from_object(app_config)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    auth.init_app(app)
    db.init_app(app)
    app.register_blueprint(auth.views.bp)

    return app
