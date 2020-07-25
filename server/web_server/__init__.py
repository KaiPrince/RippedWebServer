"""
* Project Name: RippedWebServer
* File Name: __init__.py
* Programmer: Kai Prince
* Date: Sun, Jul 19, 2020
* Description: This file contains the main entry point for the app.
"""

import os
from flask import Flask
from . import db, auth, blog, files


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "web_server.sqlite"),
        UPLOAD_FOLDER=os.path.join(app.instance_path, "uploads"),
    )

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
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(files.bp)

    app.add_url_rule("/", endpoint="index")

    return app
