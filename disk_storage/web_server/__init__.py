"""
* Project Name: RippedWebServer
* File Name: __init__.py
* Programmer: Kai Prince
* Date: Sun, Jul 19, 2020
* Description: This file contains the main entry point for the app.
"""

import os

import storage.views
from config import TestingConfig, getConfig
from flask import Flask
from storage import sockets


def create_app(test_config=None):
    # create and configure the app
    app = Flask(
        __name__,
        instance_relative_config=True,
    )

    if test_config is None:
        app_config = getConfig(app)
        app.config.from_object(app_config)
    else:
        # load the test config if passed in
        app.config.from_object(TestingConfig(app, **test_config))
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    sockets.init_app(app)
    storage.init_app(app)
    app.register_blueprint(storage.views.bp)

    app.add_url_rule("/", endpoint="index", view_func=storage.views.index)

    return app
