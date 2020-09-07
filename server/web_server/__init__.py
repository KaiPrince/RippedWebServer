"""
* Project Name: RippedWebServer
* File Name: __init__.py
* Programmer: Kai Prince
* Date: Sun, Jul 19, 2020
* Description: This file contains the main entry point for the app.
"""

import os
from flask import Flask
from .config import getConfig
import db
import files.views
import auth.views


def create_app(test_config=None):
    # create and configure the app
    app = Flask(
        __name__,
        instance_relative_config=True,
    )

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

    db.init_app(app)
    files.init_app(app)
    app.register_blueprint(auth.views.bp)
    app.register_blueprint(files.views.bp)

    app.add_url_rule("/", endpoint="index", view_func=files.views.index)

    return app
