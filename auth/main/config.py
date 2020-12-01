import logging
import os

from dotenv import find_dotenv, load_dotenv
from flask import Flask


class Config(object):

    # Import config from .env file
    load_dotenv(find_dotenv())

    # Import config from environment
    SECRET_KEY = os.getenv("SECRET_KEY")
    DATABASE = os.getenv("DATABASE")
    JWT_KEY = os.getenv("JWT_KEY")
    LOGGING_SERVICE_URL = os.getenv("LOGGING_SERVICE_URL")
    LOGGING_AUTH_TOKEN = os.getenv("LOGGING_AUTH_TOKEN")

    def __init__(self, app: Flask):

        if self.SECRET_KEY is None:
            app.logger.warning("SECRET_KEY environment variable not set.")

        if self.DATABASE is None:
            app.logger.warning("DATABASE environment variable not set.")
            self.DATABASE = os.path.join(app.instance_path, "web_server.sqlite")

        if self.JWT_KEY is None:
            app.logger.warning("JWT_KEY environment variable not set.")
            self.JWT_KEY = "dev"

        if self.LOGGING_SERVICE_URL is None:
            app.logger.warning("LOGGING_SERVICE_URL environment variable not set.")
            self.LOGGING_SERVICE_URL = "http://localhost:5005/logger/log"

        if self.LOGGING_AUTH_TOKEN is None:
            app.logger.warning("LOGGING_AUTH_TOKEN environment variable not set.")
            self.LOGGING_AUTH_TOKEN = "dev"


# class Config(object):
#     DEBUG = False
#     TESTING = False
#     DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(Config):
    # DATABASE_URI = "mysql://user@localhost/foo"
    MODE = "PRODUCTION"


class DevelopmentConfig(Config):
    MODE = "DEVELOPMENT"
    DEBUG = True

    def __init__(self, app: Flask):

        if self.SECRET_KEY is None:
            self.SECRET_KEY = "dev"

        super().__init__(app)


class TestingConfig(Config):
    MODE = "TESTING"
    TESTING = True

    def __init__(self, app: Flask):

        if self.SECRET_KEY is None:
            self.SECRET_KEY = "dev"

        super().__init__(app)


def getConfig(app: Flask):
    mode = os.getenv("FLASK_ENV")
    if mode is not None:
        mode = mode.upper()  # Normalize case

    if mode == "DEVELOPMENT":
        return DevelopmentConfig(app)
    elif mode == "PRODUCTION":
        return ProductionConfig(app)
    elif mode == "TESTING":
        return TestingConfig(app)
    else:
        app.logger.warning(
            "FLASK_ENV environment variable not set. Defaulting to DEVELOPMENT mode."
        )
        return DevelopmentConfig(app)
