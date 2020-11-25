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
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")

    def __init__(self, app: Flask):

        if self.SECRET_KEY is None:
            logging.warning("SECRET_KEY environment variable not set.")

        if self.DATABASE is None:
            logging.warning("DATABASE environment variable not set.")
            self.DATABASE = os.path.join(app.instance_path, "web_server.sqlite")

        if self.UPLOAD_FOLDER is None:
            logging.warning("UPLOAD_FOLDER environment variable not set.")
            self.UPLOAD_FOLDER = os.path.join(app.instance_path, "uploads")


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

    def __init__(self, app: Flask, UPLOAD_FOLDER=None, **kwargs):

        if self.SECRET_KEY is None:
            self.SECRET_KEY = "dev"

        if UPLOAD_FOLDER is not None:
            self.UPLOAD_FOLDER = UPLOAD_FOLDER

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
        logging.warning(
            "FLASK_ENV environment variable not set. Defaulting to DEVELOPMENT mode."
        )
        return DevelopmentConfig(app)
