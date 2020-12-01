import os

from flask import Flask

import auth
import db
import files.views

from .config import getConfig


def create_app(test_config=None):
    # create and configure the app
    app = Flask(
        __name__,
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

    db.init_app(app)
    auth.init_app(app)
    app.register_blueprint(files.views.bp)

    app.add_url_rule("/", endpoint="index", view_func=files.views.index)

    return app
