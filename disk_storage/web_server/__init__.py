"""
* Project Name: RippedWebServer
* File Name: __init__.py
* Programmer: Kai Prince
* Date: Sun, Jul 19, 2020
* Description: This file contains the main entry point for the app.
"""

import os

from flask import Flask

import storage.views
from common import periodically_do
from config import TestingConfig, getConfig
from service_api.service_registry import ServicesRepository


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

    storage.init_app(app)
    app.register_blueprint(storage.views.bp)

    app.add_url_rule("/", endpoint="index", view_func=storage.views.index)

    # Register self to service registry (every 20 seconds)
    service_repo = ServicesRepository(app.config["SERVICE_REGISTRY_URL"])
    periodically_do(service_repo.make_ping_func("disk_storage", "1.0.0"), 20.0)

    return app
